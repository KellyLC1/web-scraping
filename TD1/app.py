from flask import Flask, render_template, request, redirect, url_for
from search_articles import search_articles

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    query = request.args.get('query', '')
    articles = search_articles(query if query else None)
    return render_template('index.html', articles=articles, query=query)

if __name__ == '__main__':
    app.run(debug=True)
