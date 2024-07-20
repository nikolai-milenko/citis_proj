import requests
import json

def save_articles(host, articles):
    url = f"http://{host}/addarticles/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "articles": articles
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Articles saved successfully.")
    else:
        print(f"Failed to save articles. HTTP status code: {response.status_code}")

# Пример использования функции
# if __name__ == "__main__":
#     host = "localhost:8082"
#
#     articles = [
#         {
#             "url": "https://example.com/article1",
#             "text": "This is the text of article 1.",
#             "description": "Description of article 1."
#         },
#         {
#             "url": "https://example.com/article2",
#             "text": "This is the text of article 2.",
#             "description": "Description of article 2."
#         }
#     ]
#
#     save_articles(host, articles)
