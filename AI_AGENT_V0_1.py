from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from langchain_core.prompts import PromptTemplate


giga = GigaChat(
    # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
    credentials="YjBiMGE1YWQtMjNiMS00YTI0LTg4MGItN2NmYjYzNTE5M2RhOmRmNjM1ZGRjLThmYTEtNDViNy1iMDA0LTFmODZiMGY4NTgxNA==",
    verify_ssl_certs=False,
)


# Списки боссов и триггерных слов
BOSSES = ["Фишер", "Ларионов", "Смольянинова", "Греф"]
TRIGGER_WORDS = ["инцидент", "сбой", "авария", "блокировка"]

# Функция для чтения письма из файла
def read_email_from_file(file_path: str):
    """Считывает тему, отправителя и текст письма из файла."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    sender = lines[0].strip()
    subject = lines[2].strip()
    content = " ".join(line.strip() for line in lines[3:])
    return subject, sender, content

# Функция для анализа важности письма
def analyze_email(subject: str, sender: str, content: str) -> str:
    """Анализирует письмо и определяет его важность с учетом босса и триггерных слов."""
    sender_boss = sender in BOSSES
    trigger_word = any(word in content.lower() for word in TRIGGER_WORDS)
    
    # Определение важности письма
    if sender_boss and trigger_word:
        importance_level = "высокая"
    elif sender_boss or trigger_word:
        importance_level = "средняя"
    else:
        importance_level = "низкая"
    
    return f"Важность письма: {importance_level} (Босс: {sender_boss}, Триггерное слово: {trigger_word})"

# Пример использования
if __name__ == "__main__":
    file_path = "email_test_v1/email5.txt"  # Укажите путь к файлу с письмом
    subject, sender, content = read_email_from_file(file_path)
    importance = analyze_email(subject, sender, content)
    print("Результат анализа:", importance)


# Пример использования
# if __name__ == "__main__":
#     subject = "Срочное обновление проекта"
#     sender = "Иван Петров"
#     position = "Менеджер проекта"
#     content = "Добрый день! У нас изменились сроки сдачи проекта, необходимо срочно обсудить изменения."  
    
#     importance = analyze_email(subject, sender, position, content)
#     print("Результат анализа:", importance)

# if __name__ == "__main__":
#     subject = "АБВ или ГДЕ"
#     sender = "Иван Иванов"
#     position = "Бот уведомлений"
#     content = "Доброе утро! В сегодняшнем дайджесте узнаете, чем АБВ отличается от ГДЕ "  
    
#     importance = analyze_email(subject, sender, position, content)
#     print("Результат анализа:", importance)

#доработать: подаем только тек