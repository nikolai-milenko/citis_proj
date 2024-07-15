from better_profanity import profanity
import re

def validate_search_query(query):
    # Проверяем, что запрос не пустой
    if not query or not query.strip():
        return False

    # Проверяем на наличие цензурных слов
    if profanity.contains_profanity(query):
        return False

    return True
