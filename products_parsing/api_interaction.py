import json
import requests


def save_products(host, products_file_path):
    # Формируем URL для запроса
    url = f"http://{host}/addproducts/"
    headers = {'Content-Type': 'application/json'}

    # Загружаем продукты из JSON файла
    with open(products_file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

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