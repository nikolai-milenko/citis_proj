from flask import Flask, request, jsonify

from swagger import articles_query_model, empty_response_model, error_model
from parser import parse_article
from links_getter import get_links
import save_articles as uc
from flask_restx import Resource
from swagger import init_swagger, articles_ns
import send_to_analytics as send_to_analytics

app = Flask(__name__)
init_swagger(app)


def create_parse_handler(cfg):
    class ParseHandler(Resource):
        @articles_ns.expect(articles_query_model, validate=True)
        @articles_ns.response(200, 'Success', empty_response_model)
        @articles_ns.response(400, 'Bad Request', error_model)
        def post(self):
            if not request.json or 'query' not in request.json:
                return jsonify({"error": "No text provided"}), 400

            repo_host = cfg.get_db_host()

            text = request.json['query']
            result = []
            links = get_links(repo_host, text, cfg.get_max_hits())
            for link in links:
                text = parse_article(link)
                if text is not None and text != '':
                    result.append({'url': link, 'text': text})

            if len(result) == 0:
                return jsonify({"error": "Nothing found"}), 404

            uc.save_articles(repo_host, result)

            send_to_analytics.send_to_analytics(cfg.get_analytics_host(), repo_host, result)

    return ParseHandler


# @app.route('/parse', methods=['POST'])
# def parse():
#     if not request.json or 'query' not in request.json:
#         return jsonify({"error": "No text provided"}), 400
#
#     repo_host = 'localhost:8082'
#
#     text = request.json['query']
#     result = []
#     links = get_links(repo_host, text, 10)
#     for link in links:
#         text = parse_article(link)
#         if text is not None and text != '':
#             result.append({'url': link, 'text': text, 'description': ''})
#
#     if len(result) == 0:
#         return jsonify({"error": "Failed to parse article"}), 500
#
#     err = uc.save_articles(repo_host, result)
#
#     return jsonify({"result": result})


def run(host, port, cfg, debug=False):
    articles_ns.add_resource(create_parse_handler(cfg), '/parse')
    app.run(host=host, port=port, debug=debug)
