import requests
from bs4 import BeautifulSoup
import time
import json
import re

from urllib.parse import urlparse
import http.client

from typing import List, Dict, Union, Tuple

from products_parsing.config import *
from filter import contains_banned_words

http.client._MAXHEADERS = 1000

# параметры для поиска, впоследствии вставятся в url
params = {
    'q': '',  # query
    'gl': 'ru',  # country to search from
    'hl': 'ru',  # language
    'start': 0  # элемент начиная с которого по счету отображать результаты
}


def get_html_content(url: str):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()  # Вызываем исключение при ошибке HTTP
    return response.text


def get_element_text(soup, css_selector) -> Union[str, None]:
    element = soup.select_one(css_selector)
    return element.text.strip() if element else None


def get_elements_text(soup, css_selector) -> List[Union[str, None]]:
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


def collect_search_result(search_url: str) -> List[Dict]:
    product_websites = []
    html_text = get_html_content(search_url)
    soup = BeautifulSoup(html_text, 'lxml')

    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        if any([re.search(marketplace, link) for marketplace in marketplaces]):
            print(f'Нашелся маркетплейс: {title}, {link}')
            continue

        domain_name = get_domain_name(link)
        if any([re.search(domain_name, get_domain_name(new_product['url'])) for new_product in product_websites]):
            print(f'Нашелся уже добавленный сайт: {domain_name}')
            continue

        time.sleep(4)  # Ждём перед запросом следующей страницы
        product_websites.append({'title': title, 'link': link, 'domain_name': domain_name})
    return product_websites


def get_products_info(product_websites: List[Dict]) -> List[Dict]:
    products_data = []
    for website in product_websites:
        try:
            product_page = get_html_content(website['url'])
            if contains_banned_words(product_page):
                print(f"Страница по адресу '{website['url']}' содержит запрещённые слова и будет пропущена.")
                continue

            product_soup = BeautifulSoup(product_page, 'html.parser')

            if website['domain_name'] in websites_css_selectors.keys():
                # отлично! селекторы для этой страницы известны!
                print(f'Для сайта с доменным именем {website["domain_name"]} нашлись селекторы!')

                website_info = websites_css_selectors[website['domain_name']]

                # определяем, находимся ли мы уже на странице товара или еще только на странице с листингом товаров
                if not product_soup.select(website_info[1]['price']):
                    # находимся на странице с листингом товаров
                    products_links = product_soup.select(website_info[0])
                    for product in products_links:
                        products_data.extend(parse_product(product, website_info))
                else:
                    products_data.extend(parse_product(website['url'], website_info))
            else:
                print(f'Для сайта с доменным именем {website["domain_name"]} НЕ НАШЛОСЬ селекторов!')
                continue
        except Exception as e:
            print(f"Error parsing {website['url']}: {e}")

    return products_data


def parse_product(product_url, website_params) -> Dict:
    html_text = get_html_content(product_url)
    soup = BeautifulSoup(html_text, 'lxml')

    product_name = soup.select(website_params[1]['name'])
    if len(product_name) != 1:
        product_name = ['']

    product_price = soup.select(website_params[1]['price'])
    if len(product_price) != 1:
        product_price = ['']

    product_rating = soup.select(website_params[1]['rating'])
    if len(product_rating) != 1:
        product_rating = ['']

    product_data = {
        'name': product_name[0],
        'price': product_price[0],
        'rating': product_rating[0],
    }

    reviews_url = soup.select_one(website_params[1]['reviews'])

    product_data['reviews'] = parse_reviews(reviews_url, product_data, website_params)

    return product_data


def parse_reviews(reviews_url, product_data: Dict, website_params) -> List[Dict]:
    html_text = get_html_content(reviews_url)
    soup = BeautifulSoup(html_text, 'lxml')

    reviews = []
    for review_comment in soup.select(website_params[1]['review_comment']):
        reviews.append({'review': review_comment})

    _ = 0
    for review_rating in soup.select(website_params[1]['review_rating']):
        reviews[_]['rating'] = review_rating
        _ += 1

    return reviews


def collect_products_info(search_url: str) -> Tuple[List[Dict], List[Dict]]:
    product_websites = collect_search_result(search_url)  # сейвим результаты поиска в google
    products_data = get_products_info(product_websites)  # достаем все ссылки на товары, а по ним и инфу о продуктах
    return products_data


def parse(query):
    """
    Принимает запрос и создает json с найденными товарами и их параметрами
    :param query: текстовый запрос пользователя
    :return:
    """

    global params

    # проверка на содержание в запросе пользователя бан-вордов
    if contains_banned_words(query):
        print(f"Запрос '{query}' содержит запрещённые слова и будет отклонён.")
        return

    # в качестве поисковика используем google
    base_url = 'https://www.google.com/'
    search_url = f'https://www.google.com/search'

    cur_page = 0

    params['query'], params['start'] = query, cur_page * 10
    products_data = []

    while len(products_data) < min_results_count:
        products_data.extend(collect_products_info(search_url))
        cur_page += 1
        time.sleep(2)

    # Сохраняем данные в JSON файл
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products_data, f, ensure_ascii=False, indent=4)


# Пример использования
parse("купить машину")
