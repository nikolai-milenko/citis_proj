import requests


def is_banned(host, url, max_hits):
    # Формируем полный URL для запроса
    full_url = f"http://{host}/geturl/"

    # Формируем данные для POST запроса
    data = {
        "url": url
    }

    try:
        # Отправляем POST запрос
        response = requests.post(full_url, json=data)

        # Проверяем статус ответа
        if response.status_code == 200:

            response_data = response.json()

            hits = response_data.get('hits', 0)
            if hits > max_hits:
                return True
            else:
                return False
        else:
            print(f"Failed to get URL info. Status code: {response.status_code}")
            return True
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return False
