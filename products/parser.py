import time
import json
import re
from urllib.parse import urlencode, urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from typing import List, Dict, Union, Tuple
from config import *
from filter import contains_banned_words
import argparse
from config import Config
import api_interaction


params = {
    'q': '',  # query
    'gl': 'ru',  # country to search from
    'hl': 'ru',  # language
    'start': 0  # элемент начиная с которого по счету отображать результаты
}

# Настройка Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

service = None


def get_html_content_selenium(url: str):
    driver = webdriver.Chrome(service=service, options=options)
    url_with_params = f"{url}?{urlencode(params)}"
    driver.get(url_with_params)
    time.sleep(10)
    # Не менять, иногда сайты загружаются долго, например, мвидео, на ходу контент сует в html, т.к. написан с ajax
    html = driver.page_source
    driver.quit()
    return html


def get_element_text(soup, css_selector) -> Union[str, None]:
    element = soup.select_one(css_selector)
    return element.text.strip() if element else None


def get_elements_text(soup, css_selector) -> List[Union[str, None]]:
    elements = soup.select(css_selector)
    return [element.text.strip() for element in elements]


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def collect_search_result(search_url: str, product_websites, cfg: Config) -> List[Dict]:
    html_text = get_html_content_selenium(search_url)
    soup = BeautifulSoup(html_text, 'lxml')

    _ = 0
    for result in soup.select('.tF2Cxc'):
        title = result.select_one('.DKV0Md').text
        link = result.select_one('.yuRUbf a')['href']
        _ += 1
        if any([re.search(marketplace, link) for marketplace in cfg.get_marketplaces()]):
            print(f'Нашелся маркетплейс: {title}, {link}')
            _ -= 1
            continue

        domain_name = get_domain_name(link)
        if any([re.search(domain_name, get_domain_name(new_product['url'])) for new_product in product_websites]):
            print(f'Нашелся уже добавленный сайт: {domain_name}')
            _ -= 1
            continue

        product_websites.append({'title': title, 'url': link, 'domain_name': domain_name})
        print(f'Нашелся сайт который будем парсить! {domain_name}')
        print('Ожидание перед проверкой следующей страницы 5 с.')
        time.sleep(5)  # Ждём перед запросом следующей страницы
        if _ == cfg.get_max_websites_count():
            break

    print(f'\nДля этой страницы поиска сайты собраны! Всего собрано: {len(product_websites)}')

    return product_websites


def get_products_info(product_websites: List[Dict], cfg: Config) -> List[Dict]:
    products_data = []
    for website in product_websites:
        print(f'\n\nПроверка страницы: {website["url"]}')
        try:
            product_page = get_html_content_selenium(website['url'])
            if contains_banned_words(product_page):
                print(f"Страница по адресу '{website['url']}' содержит запрещённые слова и будет пропущена.")
                continue

            product_soup = BeautifulSoup(product_page, 'html.parser')

            if website['domain_name'] in cfg.get_website_selectors().keys():
                # отлично! селекторы для этой страницы известны!
                print(f'Для сайта с доменным именем {website["domain_name"]} нашлись селекторы!')
                time.sleep(5)

                website_info = cfg.get_website_selectors()[website['domain_name']]
                # print(f'Информация о веб-сайте с доменным именем {website["domain_name"]}: {website_info}')
                # print(product_soup)
                # print(product_soup.select(website_info[0]))
                # определяем, находимся ли мы уже на странице товара или еще только на странице с листингом товаров
                if not product_soup.select(website_info[1]['price']) or not product_soup.select(website_info[1]['reviews'] or not product_soup.select(website_info[1]['rating'])):
                    print(f'Находимся на странице с листингом товаров.')
                    # находимся на странице с листингом товаров
                    products_links = product_soup.select(website_info[0])
                    results_from_website_cnt = 0
                    for product in products_links:
                        results_from_website_cnt += 1
                        match = re.search(website["domain_name"], product['href'])
                        if match:
                            products_data.append(
                                parse_product(f'{product["href"]}', website_info))
                        else:
                            products_data.append(parse_product(f'https://{website["domain_name"]}{product["href"]}', website_info))
                        if results_from_website_cnt >= cfg.get_max_results_from_website():
                            break
                    print(f'Собрали инфу о продуктах: {products_data}')
                else:
                    print('Находимся на странице конкретного товара')
                    products_data.append(parse_product(website['url'], website_info))
            else:
                print(f'Для сайта с доменным именем {website["domain_name"]} НЕ НАШЛОСЬ селекторов!')
                continue
        except Exception as e:
            print(f"Error parsing {website['url']}: {e}")

    return products_data


def parse_product(product_url, website_params) -> Dict:
    print(f'Ищем продукт по его url: {product_url}')

    html_text = get_html_content_selenium(product_url)
    soup = BeautifulSoup(html_text, 'lxml')

    print('got product html')
    product_name = soup.select(website_params[1]['name'])
    if len(product_name) != 1:
        product_name = ['']
    else:
        product_name = [product_name[0].text]
    print('got product name')
    product_price = soup.select(website_params[1]['price'])
    if len(product_price) != 1:
        product_price = ['']
    else:
        product_price = [re.sub(r'\D', '', product_price[0].text)]
    print('got product price')
    product_rating = soup.select(website_params[1]['rating'])
    if len(product_rating) != 1:
        product_rating.append('')
        product_rating = [product_rating[0]]
    if get_domain_name(product_url) == 'www.dns-shop.ru':
        product_rating = [product_rating[0]['data-rating']]
    elif get_domain_name(product_url) == 'www.vseinstrumenti.ru':
        product_tag = product_rating[0]
        product_rating = [product_tag['value']]
    else:
        try:
            product_rating = [product_rating[0].text]
        except AttributeError:
            pass

    print('got product rating')
    # print(product_name, product_price, product_rating)
    product_data = {
        'url': product_url,
        'name': product_name[0],
        'price': product_price[0],
        'rating': product_rating[0],
    }

    reviews_url = soup.select_one(website_params[1]['reviews'])
    if reviews_url is None:
        print('Ссылки на отзывы не нашли, видимо отзывов нет...')
        product_data['reviews'] = []
    else:
        try:
            product_data['reviews'] = parse_reviews(f'https://{get_domain_name(product_url)}{reviews_url["href"]}', product_data, website_params)
        except:
            product_data['reviews'] = []
            print('Ссылку на отзывы нашли, но отзывов нет...')

    # print(f'Собрали данные о продукте: {product_data}')

    return product_data


def parse_reviews(reviews_url, product_data: Dict, website_params) -> List[Dict]:
    html_text = get_html_content_selenium(reviews_url)
    soup = BeautifulSoup(html_text, 'lxml')

    print("Теперь парсим отзывы для этого сайта.")
    # print(reviews_url)
    reviews = []
    comments = soup.select(website_params[1]['review_comment'])
    print(f"Ищем по селектору: {website_params[1]['review_comment']}")
    # print(f'Комментарии: {comments}')
    for review_comment in comments:
        reviews.append({'review': review_comment.text})

    print(f'Всего отзывов: {len(reviews)}')

    _ = 0
    review_ratings = soup.select(website_params[1]['review_rating'])

    if get_domain_name(reviews_url) == 'ru-mi.com':
        review_ratings = [rating['data-rating'] for rating in review_ratings]
    elif get_domain_name(reviews_url) == 'www.rbt.ru':
        review_ratings = [rating['content'] for rating in review_ratings]
    else:
        review_ratings = [rating.text for rating in review_ratings]

    for review_rating in review_ratings:
        reviews[_]['review_rating'] = review_rating
        _ += 1
        if _ == len(reviews):
            break

    return reviews


def collect_products_info(search_url: str, cfg: Config) -> Tuple[List[Dict], List[Dict]]:
    product_websites = []
    while len(product_websites) < cfg.get_max_websites_count():
        print(f'Поиск на странице google: {params["start"] // 10 + 1}')
        product_websites = collect_search_result(search_url, product_websites, cfg)  # сейвим результаты поиска в google
        params['start'] += 10
        time.sleep(10)
    print(f'\nПолучили: {product_websites}')
    print('Теперь ищем инфу о товарах')
    products_data = get_products_info(product_websites, cfg)  # достаем все ссылки на товары, а по ним и инфу о продуктах
    return products_data

# Обновляет инфу о тех продуктах, урлы которых были переданы, пишет в файл updated_products.json
def update_products_info(cfg: Config):
    print("Начинаем обновление информации о продуктах...")
    
    # Получаем URL-адреса из сервиса
    product_urls = api_interaction.get_urls(cfg.get_db_host())
    if product_urls is None or len(product_urls) == 0:
        print("Не удалось получить URL-адреса продуктов. Обновление прервано.")
        return

    # Создаем список словарей с URL и доменными именами
    product_websites = [{'url': url, 'domain_name': get_domain_name(url)} for url in product_urls]

    # Обновляем информацию о продуктах
    updated_products = get_products_info(product_websites)

    # Сохраняем обновленные данные в JSON файл
    with open('updated_products.json', 'w', encoding='utf-8') as f:
        json.dump(updated_products, f, ensure_ascii=False, indent=4)

    api_interaction.send_to_analytics(cfg.get_analytics_host(), updated_products)
    

def parse(query, cfg: Config):
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

    query += ' intitle:"м видео" OR intitle:"dns" OR intitle:"технопарк" OR intitle:"ситилинк"'

    params['query'], params['start'] = query, cur_page * 10

    products_data = collect_products_info(search_url, cfg)

    print(f'Результат перед упаковкой: {products_data}')

    # Сохраняем данные в JSON файл
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products_data, f, ensure_ascii=False, indent=4)

    return products_data

def init_service(path_to_driver):
    global service

    service = webdriver.chrome.service.Service(path_to_driver)
