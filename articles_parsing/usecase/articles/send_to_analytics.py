import requests
import json
from articles_parsing.usecase.blacklist.add_hit import add_hit


def send_to_analytics(host, articles):
    url = f"http://{host}/analyze_articles"
    headers = {'Content-Type': 'application/json'}

    repoURL = "localhost:8082"

    # Формируем данные для отправки
    data = {
        "articles": articles
    }

    try:
        # Отправляем POST запрос на сервер
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Проверяем статус код ответа
        response.raise_for_status()  # выбрасывает исключение для кода ответа 4xx/5xx

        # Обрабатываем ответ от сервера
        response_data = response.json()

        if isinstance(response_data, list):
            print("Received URLs:", response_data)
            for url in response_data:
                add_hit(repoURL, url)
        else:
            print("Unexpected response format:", response_data)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")


# Пример использования функции
if __name__ == "__main__":
    host = "0.0.0.0:5000"

    articles = [
        {
            "url": "https://example.com/article1",
            "text": "This is the text of article 1.",
            "description": "Description of article 1."
        },
        {
            "url": "https://example.com/article2",
            "text": "This is the text of article 2.",
            "description": "Description of article 2."
        }
    ]

    send_to_analytics(host, articles)
