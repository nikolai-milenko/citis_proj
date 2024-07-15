from query_validation import validate_search_query
from links_getter import get_google_search_results
from parser import parse_article

query = input("Enter your search query: ", )
if (validate_search_query(query)):
    links = get_google_search_results(query, pages=3)

data = []
for url in links:
    res = parse_article(url)
    if res is not None:
        data.append({'url': url, 'content': parse_article(url)})

for data in data:
    print('url:', data['url'])
    print('content:', data['content'])

# print(parse_article("https://audiomovers.com/news_omnibus_update/"))