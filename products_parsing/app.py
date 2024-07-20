from flask import Flask, request, jsonify
import parser
import api_interaction
from config import Config
import argparse

app = Flask(__name__)
def create_parse_handler(cfg):
    def handler():
        if not request.json or 'query' not in request.json:
            return jsonify({"error": "No text provided"}), 400

        text = request.json['query']
        result = []

        data = parser.parse(text, cfg)

        if len(result) == 0:
            return jsonify({"error": "Failed to parse article"}), 500

        api_interaction.save_products(cfg.get_db_host(), data)

        api_interaction.send_to_analytics(cfg.get_analytics_host(), data)

    return handler

def main():
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
    # Пример использования

    app.add_url_rule('/parse', view_func=create_parse_handler(cfg), methods=['POST'])

    host = cfg.get_server_host()
    app.run(host=host['host'], port=host['port'], debug=False)



if __name__ == '__main__':
    main()