import requests
from bs4 import BeautifulSoup
import nltk

nltk.download('punkt')

def clean_text(text):
    return ' '.join(text.split())

def extract_text_elements(soup):
    text_elements = []

    def recursive_extract(element, parent_text=""):
        for child in element.children:
            if child.name in ['div', 'p', 'span', 'article']:  # Добавляем нужные теги для поиска текста
                recursive_extract(child)
            elif child.name is None:
                parent_text += child.strip() + " "

        if len(parent_text.strip()) > 1:
            text_elements.append(parent_text.strip())

    # Начинаем с верхнего уровня элементов
    for element in soup.find_all(['p', 'span', 'article'], recursive=True):
        recursive_extract(element)

    # print(text_elements)

    return text_elements


def find_largest_text_block(text_elements):
    max_words = 0
    max_text = ""
    for text in text_elements:
        word_count = len(text.split())
        dot_count = text.count('.')
        if word_count > max_words and dot_count > 0:
            max_words = word_count
            max_text = text
    return max_text

def is_relevant(text):
    # Простая проверка на релевантность
    words = nltk.word_tokenize(text)
    num_words = len(words)
    num_dots = text.count('.')
    if num_words > 10 and num_dots > 0:  # Пороговые значения можно настроить
        return True
    return False

def combine_relevant_texts(text_blocks):
    relevant_texts = [text for text in text_blocks if is_relevant(text)]
    combined_text = ' '.join(relevant_texts)
    return combined_text


def parse_article(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        print(f"Timeout error for URL: {url}")
        return None
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    text_elements = extract_text_elements(soup)
    combined_text = combine_relevant_texts(text_elements)

    return combined_text
