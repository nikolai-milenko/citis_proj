from flask import Flask, request, jsonify
import parser
import api_interaction
from config import Config
import argparse
import threading
from swagger import init_swagger, products_ns, products_query_model, product_model
from scheduler import run_scheduler
import os

app = Flask(__name__)
from flask_restx import Resource, Namespace


# Assuming products_ns is an instance of Namespace from Flask-RESTx

def create_parse_handler(cfg):
    class ParseHandler(Resource):
        @products_ns.expect(products_query_model, validate=True)
        @products_ns.response(200, 'Success')
        @products_ns.response(400, 'Bad Request')
        def post(self):
            if not request.json or 'query' not in request.json:
                return {"error": "No text provided"}, 400

            text = request.json['query']

            data = parser.parse(text, cfg)

            if len(data) == 0:
                return {"error": "Sorry, nothing found"}, 404

            api_interaction.save_products(cfg.get_db_host(), data)
            api_interaction.send_to_analytics(cfg.get_analytics_host(), data)
            return {"data": data}, 200

    return ParseHandler


def list_files_in_directory(directory='.'):
    """Выводит список файлов в указанной директории."""
    try:
        files = os.listdir(directory)
        print(f"Файлы в директории '{directory}':")
        for file in files:
            print(file)
    except Exception as e:
        print(f"Ошибка при получении списка файлов: {e}")


def main():
    # list_files_in_directory()
    argparser = argparse.ArgumentParser(description='Run the Flask server with specified configuration file.')
    argparser.add_argument('--cfg', type=str, required=True, help='Path to the configuration file')
    args = argparser.parse_args()
    config_path = args.cfg
    cfg = Config(config_path)

    marketplaces = cfg.get_marketplaces()
    max_websites_count = cfg.get_max_websites_count()
    max_results_from_website = cfg.get_max_results_from_website()
    headers = cfg.get_headers()
    website_selectors = cfg.get_website_selectors()

    parser.init_service(cfg.get_driver_path())

    print("Маркетплейсы:", marketplaces)
    print("Максимальное количество сайтов:", max_websites_count)
    print("Максимальное количество результатов с одного сайта:", max_results_from_website)
    print("Заголовки:", headers)
    print("CSS селекторы для сайтов:", website_selectors)

    # Register the ParseHandler with Flask-RESTx
    products_ns.add_resource(create_parse_handler(cfg), '/parse')

    scheduler_thread = threading.Thread(target=run_scheduler, args=(cfg,))
    scheduler_thread.start()

    host = cfg.get_server_host()
    init_swagger(app)
    app.run(host=host['host'], port=host['port'], debug=False)


if __name__ == '__main__':
    main()
