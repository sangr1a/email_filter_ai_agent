from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from langchain_core.prompts import PromptTemplate
from db import fetch_bosses, fetch_trigger_words, fetch_prompt


giga = GigaChat(
    # Для авторизации запросов используйте ключ, полученный в проекте GigaChat API
    credentials="YjBiMGE1YWQtMjNiMS00YTI0LTg4MGItN2NmYjYzNTE5M2RhOjdmN2U5MzRkLTQ2YzYtNDNmYy05MTQ4LTI0NjM4MjFjOGQ0Mw==",
    verify_ssl_certs=False,
)

instruction="1. если отключаем боевой сервер - предварительно уведомляем сотрудников по почте. 2. отключения можно производить строго с 18:00 до 06:00. 3. кратко опишите возникшую проблему простым языком. 4.придерживайтесь принципа деловой переписки"

# Функция для чтения письма из файла
def read_email_from_file(file_path: str):
    """Считывает тему, отправителя и текст письма из файла, независимо от количества пустых строк."""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines() if line.strip()]  # Убираем пустые строки

    if len(lines) < 3:
        raise ValueError("Файл должен содержать минимум 3 строки: отправителя, тему и текст письма.")

    sender = lines[0]  # Первая непустая строка — отправитель
    subject = lines[1]  # Вторая непустая строка — тема письма
    content = " ".join(lines[2:])  # Все остальное — тело письма

    return subject, sender, content


# Функция для анализа важности письма
def analyze_email(subject: str, sender: str, content: str):
    """Анализ письма с учетом данных из БД"""
    BOSSES = fetch_bosses()
    TRIGGER_WORDS = fetch_trigger_words()

    sender_boss = sender in BOSSES
    trigger_word = any(word in content.lower() for word in TRIGGER_WORDS)

    # Определяем тип письма
    if sender_boss and trigger_word:
        label = "mail_boss_and_trigger"
    elif sender_boss:
        label = "mail_boss"
    elif trigger_word:
        label = "mail_trigger"
    else:
        label = "mail_simple"

    prompt_text = fetch_prompt(label)

    if prompt_text:
        response = giga([HumanMessage(content=prompt_text)])
        return f"Маркировка: {label}\nОтвет GigaChat: {response.content}"
    else:
        return f"Маркировка: {label} (Нет необходимости в ответе)"
    
file_path = "email_test_v1/email3.txt"  # Укажите путь к файлу с письмом
subject, sender, content = read_email_from_file(file_path)
result = analyze_email(subject, sender, content)
print("Результат анализа:", result)
