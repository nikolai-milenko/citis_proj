marketplaces = [
    'ozon',
    'wildberries',
    'market.yandex',
    'megamarket',
    'lamoda',
    'dns',
    'eldorado',
    'mvideo',
]

min_results_count = 5  # не рекомендуется выставлять значение больше 10

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