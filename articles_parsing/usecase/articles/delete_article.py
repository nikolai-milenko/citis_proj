import requests
import json
def delete_article(host, article):
    url = f"http://{host}/deletearticle/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "url": article
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        print("Article deleted successfully.")
    else:
        print(f"Failed to delete article. HTTP status code: {response.status_code}")