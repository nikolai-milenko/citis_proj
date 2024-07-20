from flask import Flask, request, jsonify
from parser import parse_article
from links_getter import get_links
import usecase.articles.save_articles as uc

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def parse():
    if not request.json or 'query' not in request.json:
        return jsonify({"error": "No text provided"}), 400

    repo_host = 'localhost:8082'

    text = request.json['query']
    result = []
    links = get_links(repo_host, text, 10)
    for link in links:
        text = parse_article(link)
        if text is not None and text != '':
            result.append({'url': link, 'text': text, 'description': ''})

    if len(result) == 0:
        return jsonify({"error": "Failed to parse article"}), 500

    err = uc.save_articles(repo_host, result)

    return jsonify({"result": result})


def run(host, port, debug=False):
    app.run(host=host, port=port, debug=debug)
