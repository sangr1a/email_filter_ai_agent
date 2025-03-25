import os
import psycopg2

# Настройки подключения к БД
DB_CONFIG = {
    "dbname": "email_ai",
    "user": "postgres",  # Замени на свой логин
    "password": "admin",  # Укажи свой пароль
    "host": "localhost",
    "port": "5432",
}

def get_db_connection():
    """Создает подключение к базе данных"""
    return psycopg2.connect(**DB_CONFIG)

def fetch_bosses():
    """Получает список боссов из базы"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM bosses;")
    bosses = [row[0] for row in cursor.fetchall()]
    conn.close()
    return bosses

def fetch_trigger_words():
    """Получает список триггерных слов из базы"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT word FROM trigger_words;")
    words = [row[0] for row in cursor.fetchall()]
    conn.close()
    return words

def fetch_prompt(label):
    """Получает соответствующий промпт по метке"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prompt FROM prompts WHERE label = %s;", (label,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""
