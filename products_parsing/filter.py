# filter.py

import re


def load_banned_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file if line.strip()]


# Загрузить запрещённые слова из файла
banned_words = load_banned_words('ban_words_ru.txt')


def contains_banned_words(text):
    """
    Проверяет, содержит ли текст запрещённые слова.

    :param text: Строка текста для проверки
    :return: True, если содержит запрещённые слова, иначе False
    """
    return any(re.search(rf'\b{re.escape(word)}\b', text, re.IGNORECASE) for word in banned_words)