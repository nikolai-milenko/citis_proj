from flask import Flask, request, jsonify

app = Flask(__name__)

# Пример списка URL для ответа
example_urls = [
    "https://example.com/result1",
    "https://example.com/result2",
    "https://example.com/result3"
]

@app.route('/analyze_articles', methods=['POST'])
def analyze_articles():
    if not request.is_json:
        return jsonify({"error": "Invalid content type, expected application/json"}), 400

    data = request.get_json()

    if 'articles' not in data or not isinstance(data['articles'], list):
        return jsonify({"error": "Invalid request, expected a list of articles"}), 400

    # Логика обработки статей и формирования ответа с URL
    # Для простоты примера возвращаем статический список URL
    return jsonify(example_urls), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
