import requests
from links_getter import get_domain_from_url


def add_hit(host, url):
    full_url = f"http://{host}/addhit/"

    # Формируем данные для POST запроса
    data = {
        "url": get_domain_from_url(url)
    }

    try:
        # Отправляем POST запрос
        response = requests.post(full_url, json=data)

        # Проверяем статус ответа
        response_data = response.json()

        if response.status_code != 200:
            print(f"Failed to add hit. Status code: {response.status_code}, error: {response_data['error']}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
