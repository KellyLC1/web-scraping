import scrapy
import csv
from pymongo import MongoClient


class KboSpider(scrapy.Spider):
    name = "kbo_spider"

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Accept-Language': 'fr-FR',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    }

    def __init__(self):
        # Connexion MongoDB
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["entreprises"]
        self.collection = self.db["kbo"]

    def start_requests(self):
        with open("entreprises.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                numero = row["numero_entreprise"]
                url = f"https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?lang=fr&nummer={numero}&actionLu=Rechercher"
                yield scrapy.Request(
                    url,
                    meta={"numero": numero},
                    callback=self.parse
                )

    def parse(self, response):
        numero = response.meta["numero"]
        entreprise = {
            "numero_entreprise": numero,
            "generalites": {},
            "fonctions": [],
            "capacites_entrepreneuriales": [],
            "qualites": [],
            "autorisations": [],
            "nace_codes": [],
            "donnees_financieres": [],
            "liens_entites": [],
            "liens_externes": []
        }

        # Extraire les "Généralités"
        generalites_rows = response.css("tr")
        for row in generalites_rows:
            key = row.css("td.QL::text").get()
            value = row.css("td.QL + td *::text").get()
            if key and value:
                entreprise["generalites"][key.strip(":")] = value.strip()
        print("Généralités extraites :", entreprise["generalites"])

        # Extraire les "Fonctions"
        fonction_rows = response.css("table#toonfctie tbody tr")
        for row in fonction_rows:
            fonction = row.css("td:nth-child(1)::text").get()
            titulaire = row.css("td:nth-child(2)::text").get()
            depuis = row.css("td:nth-child(3) .upd::text").get()
            if fonction and titulaire:
                entreprise["fonctions"].append({
                    "fonction": fonction.strip(),
                    "titulaire": titulaire.strip(),
                    "depuis": depuis.strip() if depuis else None
                })
        print("Fonctions extraites :", entreprise["fonctions"])

        # Extraire les "Capacités entrepreneuriales"
        capacites_rows = response.xpath("//h2[contains(text(), 'Capacités entrepreneuriales')]/following-sibling::tr")
        for row in capacites_rows:
            capacite = row.xpath("td/text()").get()
            if capacite:
                entreprise["capacites_entrepreneuriales"].append(capacite.strip())
        print("Capacités entrepreneuriales extraites :", entreprise["capacites_entrepreneuriales"])

        # Extraire les "Qualités"
        qualites_rows = response.xpath("//h2[contains(text(), 'Qualités')]/following-sibling::tr")
        for row in qualites_rows:
            qualite = row.xpath("td/text()").get()
            if qualite:
                entreprise["qualites"].append(qualite.strip())
        print("Qualités extraites :", entreprise["qualites"])

        # Extraire les "Autorisations"
        autorisations_rows = response.xpath("//h2[contains(text(), 'Autorisations')]/following-sibling::tr")
        for row in autorisations_rows:
            lien = row.xpath("td/a/@href").get()
            if lien:
                entreprise["autorisations"].append(lien.strip())
        print("Autorisations extraites :", entreprise["autorisations"])

        # Extraire les "Activités TVA Code Nacebel"
        nace_rows = response.xpath("//h2[contains(text(), 'Activités TVA Code Nacebel')]/following-sibling::tr")
        for row in nace_rows:
            code = row.xpath("td/a/text()").get()
            description = row.xpath("td/text()").getall()
            description = " ".join([desc.strip() for desc in description if desc.strip()])
            if code and description:
                entreprise["nace_codes"].append({
                    "code": code,
                    "description": description
                })
        print("Codes NACEBEL extraits :", entreprise["nace_codes"])

        # Sauvegarder dans MongoDB
        self.collection.update_one(
            {"numero_entreprise": numero},
            {"$set": entreprise},
            upsert=True
        )
        print(f"Données sauvegardées pour l'entreprise : {numero}")