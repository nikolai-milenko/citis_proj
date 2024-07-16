import requests
from bs4 import BeautifulSoup
import time
import json
import re

from urllib.parse import urlparse
import http.client

from typing import List, Dict

from products_parsing.config import *
from filter import contains_banned_words


http.client._MAXHEADERS = 1000


def get_html_content(url):
    response = requests.get(url)
    response.raise_for_status()  # Вызываем исключение при ошибке HTTP
    return response.text


def get_element_text(soup, css_selector):
    element = soup.select_one(css_selector)
    return element.text.strip() if element else None


def get_elements_text(soup, css_selector):
    elements = soup.select(css_selector)
    return [element.text.strip() for element in elements]


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc  # Получаем доменное имя с поддоменом, если он есть

    # Используем регулярное выражение для извлечения основного доменного имени
    match = re.search(r'(?<=\.)?([a-zA-Z0-9-]+)(?=\.[a-z]{2,})', domain)
    if match:
        return match.group(1)
    return None


def collect_products(search_url: str, headers_: Dict, params: Dict, data: List[Dict]) -> List[Dict]:
    response = requests.get(search_url, headers=headers_, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')

    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        if any([re.search(marketplace, link) for marketplace in marketplaces]):
            print(f'Нашелся маркетплейс: {title}, {link}')
            continue

        domain_name = get_domain_name(link)
        if any([re.search(domain_name, get_domain_name(new_product['url'])) for new_product in data]):
            print(f'Нашелся уже добавленный сайт: {domain_name}')
            continue

        time.sleep(4)  # Ждём перед запросом следующей страницы
        try:
            product_page = get_html_content(link)
            if contains_banned_words(product_page):
                print(f"Страница по адресу '{link}' содержит запрещённые слова и будет пропущена.")
                continue
            product_soup = BeautifulSoup(product_page, 'html.parser')

            name = get_element_text(product_soup, 'название_товара_css')
            description = get_element_text(product_soup, 'описание_товара_css')
            price = get_element_text(product_soup, 'цена_товара_css')
            evaluation = get_element_text(product_soup, 'оценка_товара_css')
            reviews_elements = product_soup.select('отзывы_css')
            reviews_data = []
            for review in reviews_elements:
                review_evaluation = get_element_text(review, 'оценка_отзыва_css')
                review_text = get_element_text(review, 'текст_отзыва_css')
                reviews_data.append({
                    'evaluation': review_evaluation,
                    'review': review_text
                })

            data.append({
                'url': link,
                'name': name,
                'description': description,
                'price': price,
                'evaluation': evaluation,
                'reviews': reviews_data
            })
        except Exception as e:
            print(f"Error parsing {link}: {e}")
    return data


def parse(query):
    if contains_banned_words(query):
        print(f"Запрос '{query}' содержит запрещённые слова и будет отклонён.")
        return
    base_url = 'https://www.google.com/'
    search_url = f'https://www.google.com/search'

    cur_page = 0

    params = {
        'q': query,  # query
        'gl': 'ru',  # country to search from
        'hl': 'ru',  # language
        'start': cur_page * 10
    }
    product_data = []

    while len(product_data) < min_results_count:
        product_data = collect_products(search_url, headers, params, product_data)
        cur_page += 1
        time.sleep(2)

    # Сохраняем данные в JSON файл
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)


# Пример использования
parse("купить машину")
