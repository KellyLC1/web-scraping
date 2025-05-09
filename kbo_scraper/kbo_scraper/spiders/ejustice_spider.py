import scrapy
import csv
from pymongo import MongoClient


class EjusticeSpider(scrapy.Spider):
    name = "ejustice_spider"

    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["entreprises"]
        self.collection = self.db["ejustice"]

    def start_requests(self):
        with open("entreprises.csv", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                numero = row["numero_entreprise"]
                url = f"https://www.ejustice.just.fgov.be/cgi_list/list.pl?btw={numero}&language=fr"
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={"numero": numero}
                )

    def parse(self, response):
        numero = response.meta["numero"]
        publications = []

        for item in response.css("div.list-item"):
            texte = item.css(".list-item--content").xpath("string()").get()
            texte = texte.replace("\xa0", " ").strip()

            lignes = texte.split("\n")
            lignes = [l.strip() for l in lignes if l.strip()]

            if len(lignes) >= 4:
                publication = {
                    "raison_sociale": lignes[0],
                    "adresse": lignes[1],
                    "numero_bce": lignes[2],
                    "type_publication": lignes[3],
                    "date_reference": lignes[4] if len(lignes) > 4 else None,
                }

                image_url = item.css("a[href$='.pdf']::attr(href)").get()
                if image_url:
                    publication["url_image"] = response.urljoin(image_url)
                else:
                    publication["url_image"] = None

                publications.append(publication)

        self.collection.update_one(
            {"numero_entreprise": numero},
            {"$set": {"publications": publications}},
            upsert=True
        )
