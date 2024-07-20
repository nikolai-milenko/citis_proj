import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from usecase.blacklist.is_banned import is_banned

import time
import re


def get_google_search_results(query, pages=10, time_filter='m'):  # 'm' for month
    query += " статья"
    query = query.replace(' ', '+')
    base_url = f"https://www.google.com/search?q={query}&tbs=qdr:{time_filter}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    search_results = set()

    for page in range(1, pages + 1):
        start = page * 10
        url = f"{base_url}&start={start}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for g in soup.find_all('div', class_='tF2Cxc'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    search_results.add(link)  # todo проверка что все страницы просмотрены

            # Проверяем наличие ссылки на следующую страницу
        else:
            print(f"Error: {response.status_code}")
            break

    return search_results


def get_links(repository_host, query, max_hits):
    links = get_google_search_results(query, pages=3, time_filter='m')

    for link in links:
        res = is_banned(repository_host, link, max_hits)
        if res:
            link.delete(link)

    return links


def get_domain_from_url(url):
    # Разбираем URL с помощью urlparse
    parsed_url = urlparse(url)
    # Возвращаем доменное имя
    return parsed_url.netloc
