marketplaces = [
    'ozon',
    'wildberries',
    'market.yandex',
    'megamarket',
    'lamoda',
    'dns',
    'eldorado',
    'mvideo',
    'google',
]

min_results_count = 5  # не рекомендуется выставлять значение больше 10

max_results_from_website = 10  # максимальное количество товаров, полученное в итоге с одного сайта

'''
некоторые сайты возвращают код 403 - не дают доступ в связи с неправдоподобными headers
методом подбора оставлена конфигурация, работающая для большинства случаев

некоторые сайты возвращают код 401, чаще всего делая редирект на страницу с капчей - это обойти невозможно
'''

headers = {
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    # 'Accept-Encoding': "gzip, deflate, br, zstd",
    # 'Accept-Language': "de,en-US;q=0.7,en;q=0.3",
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
}

websites_css_selectors = {
    'www.citilink.ru': ['a.app-catalog-9gnskf.e1259i3g0', {'name': '.easmdi50.eml1k9j0.app-catalog-lc5se5.e1gjr6xo0', 'price': '.e1j9birj0.e106ikdt0.app-catalog-8hy98m.e1gjr6xo0', 'rating': '.e8eovjk0.app-catalog-1uwfsq8.e2kybqa2', 'reviews': 'a.app-catalog-peotpw.e1mnvjgw0', 'review_rating': '.e1ys5m360.e106ikdt0.app-catalog-rx1cfc.e1gjr6xo0', 'review_comment': 'e1ys5m360.e106ikdt0.app-catalog-rx1cfc.e1gjr6xo0'}],

}
