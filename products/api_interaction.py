import json
import requests

def get_urls(host):
    service_url = f"http://{host}/geturls" 
    try:
        response = requests.post(service_url)
        response.raise_for_status()  # Вызовет исключение для неуспешных статус-кодов
        data = response.json()
        if data.get("error"):
            print(f"Ошибка при получении URL-адресов: {data['error']}")
            return None
        return data.get("urls", [])
    except requests.RequestException as e:
        print(f"Ошибка при запросе к сервису: {e}")
        return None
    
def save_products(host, products):
    # Формируем URL для запроса
    url = f"http://{host}/addproducts/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "products": products
    }

    # Отправляем POST запрос
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except:
        print("Не удалось сохранить продукты.")

    # Проверяем статус код ответа
    if response.status_code == 200:
        print("Продукты успешно сохранены.")
    else:
        print(f"Не удалось сохранить продукты. Код статуса HTTP: {response.status_code}")


def send_to_analytics(host, products):
    # Формируем URL для запроса
    url = f"http://{host}/analyzeproducts/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "products": products
    }

    # Отправляем POST запрос
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # Проверяем статус код ответа
        if response.status_code == 200:
            print("Продукты успешно сохранены.")
        else:
            print(f"Не удалось сохранить продукты. Код статуса HTTP: {response.status_code}")
    except:
        print("Не удалось отправить данные в аналитику.")
