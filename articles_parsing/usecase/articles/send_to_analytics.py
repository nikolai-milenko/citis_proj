import requests
import json
from articles_parsing.usecase.blacklist.add_hit import add_hit


def send_to_analytics(analytics_host, repo_host, articles):
    url = f"http://{analytics_host}/analyze_articles"
    headers = {'Content-Type': 'application/json'}

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
                add_hit(repo_host, url)

        else:
            print("Unexpected response format:", response_data)

    except:
        print("Не удалось отправить данные аналитике")


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
