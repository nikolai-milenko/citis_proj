# этот скрипт ищет топ-50 самых встречающихся сайтов по запросам поиска продуктов

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import Counter
import time
from typing import List, Dict
from config import marketplaces


def get_html_content(url, headers, params):
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.text


def get_domain_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    return domain


def is_marketplace(domain):
    return any(marketplace in domain for marketplace in marketplaces)


def extract_domains_from_search_results(query, headers, num_pages=5):
    domains = []
    for page in range(num_pages):
        params = {
            'q': query,
            'gl': 'ru',
            'hl': 'ru',
            'start': page * 10
        }
        html_content = get_html_content('https://www.google.com/search', headers, params)
        soup = BeautifulSoup(html_content, 'html.parser')
        search_results = soup.select('a[href^="http"]')
        for link in search_results:
            url = link.get('href')
            domain = get_domain_name(url)
            if not is_marketplace(domain):
                domains.append(domain)
        time.sleep(1)  # Добавляем задержку, чтобы избежать блокировки
    return domains


def get_top_domains(queries: List[str], headers, num_pages=3, top_n=50) -> Dict[str, int]:
    all_domains = []
    for query in queries:
        domains = extract_domains_from_search_results(query, headers, num_pages)
        all_domains.extend(domains)
        time.sleep(20)

    domain_counter = Counter(all_domains)
    return dict(domain_counter.most_common(top_n))


def save_to_file(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for domain, count in data.items():
            f.write(f"{domain}: {count}\n")


# Пример использования
if __name__ == "__main__":
    queries = [
        "купить микроволновку",
        "купить телевизор",
        "купить холодильник",
        "купить стиральную машину",
        "купить ноутбук",
        "купить смартфон",
        "купить планшет",
        "купить пылесос",
        "купить кондиционер",
        "купить утюг",
        "купить газовую плиту",
        "купить электрическую плиту",
        "купить посудомоечную машину",
        "купить кухонный комбайн",
        "купить мультиварку",
        "купить блендер",
        "купить мясорубку",
        "купить чайник",
        "купить кофеварку",
        "купить тостер",
        "купить соковыжималку",
        "купить холодильную витрину",
        "купить морозильную камеру",
        "купить духовой шкаф",
        "купить вытяжку",
        "купить водонагреватель",
        "купить миксер",
        "купить хлебопечку",
        "купить пылесос-робот",
        "купить осушитель воздуха",
        "купить увлажнитель воздуха",
        "купить обогреватель",
        "купить электрокамин",
        "купить очиститель воздуха",
        "купить кондиционер мобильный",
        "купить радиатор",
        "купить термопот",
        "купить вентилятор",
        "купить стайлер для волос",
        "купить плойку",
        "купить выпрямитель для волос",
        "купить фен",
        "купить триммер",
        "купить машинку для стрижки",
        "купить эпилятор",
        "купить массажер",
        "купить весы",
        "купить зубную щетку",
        "купить ирригатор",
        "купить телевизор OLED"
    ]

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0"
    }

    top_domains = get_top_domains(queries, headers)
    save_to_file(top_domains, 'top_domains.txt')
    print("Топ-50 доменов успешно сохранены в 'top_domains.txt'")
