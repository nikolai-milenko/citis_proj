import json
import requests


def save_products(host, products):
    # Формируем URL для запроса
    url = f"http://{host}/addproducts/"
    headers = {'Content-Type': 'application/json'}

    data = {
        "products": products
    }

    # Отправляем POST запрос
    response = requests.post(url, headers=headers, data=json.dumps(data))

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
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверяем статус код ответа
    if response.status_code == 200:
        print("Продукты успешно сохранены.")
    else:
        print(f"Не удалось сохранить продукты. Код статуса HTTP: {response.status_code}")