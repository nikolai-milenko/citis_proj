import requests
import json

def save_articles(host, articles):
    url = f"http://{host}/addarticles/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "articles": articles
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except:
        print("Не удалось сохранить статьи")
        return

    if response.status_code == 200:
        print("Статьи успешно сохранены")
    else:
        print(f"Failed to save articles. HTTP status code: {response.status_code}")
