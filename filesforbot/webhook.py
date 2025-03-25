# import json
# import requests
# import psycopg2
# from flask import Flask, request, jsonify

# # Настройки API Сбера
# SBER_BOT_ID = "823330613"
# SBER_ACCESS_TOKEN = "e8a7f95519e667b64991fe0c0a9d25b3bf9e3d2d"
# SBER_WEBHOOK_URL = f"https://smartapp-code.sber.ru/webhook/{SBER_BOT_ID}"

# # Настройки базы данных PostgreSQL
# DB_CONFIG = {
#     "dbname": "email_ai",
#     "user": "postgres",
#     "password": "admin",
#     "host": "localhost"
# }

# app = Flask(__name__)

# # Подключение к БД
# def get_db_connection():
#     return psycopg2.connect(**DB_CONFIG)

# # Функция для анализа письма
# def analyze_email(sender, content):
#     conn = get_db_connection()
#     cur = conn.cursor()

#     # Загружаем данные из базы
#     cur.execute("SELECT name FROM bosses")
#     bosses = [row[0] for row in cur.fetchall()]

#     cur.execute("SELECT word FROM trigger_words")
#     trigger_words = [row[0] for row in cur.fetchall()]

#     cur.execute("SELECT type, prompt FROM prompts")
#     prompts = {row[0]: row[1] for row in cur.fetchall()}

#     conn.close()

#     sender_boss = sender in bosses
#     trigger_word = any(word in content.lower() for word in trigger_words)

#     if sender_boss and trigger_word:
#         prompt_type = "mail_boss_and_trigger"
#     elif sender_boss:
#         prompt_type = "mail_boss"
#     elif trigger_word:
#         prompt_type = "mail_trigger"
#     else:
#         prompt_type = None

#     if prompt_type:
#         return prompts.get(prompt_type, "Нет подходящего промпта")
#     else:
#         return "mail_simple"

# # Отправка ответа обратно в СберЧат
# def send_response_to_sber(user_id, message):
#     headers = {
#         "Authorization": f"Bearer {SBER_ACCESS_TOKEN}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "messageName": "ANSWER_TO_USER",
#         "sessionId": user_id,
#         "payload": {
#             "pronounceText": message,
#             "text": message
#         }
#     }
#     response = requests.post(SBER_WEBHOOK_URL, headers=headers, json=data)
#     return response.json()

# # Вебхук для приема сообщений
# @app.route("/webhook", methods=["POST"])
# def webhook():
#     data = request.json

#     user_id = data["session"]["userId"]
#     sender = data["payload"]["sender"]
#     content = data["payload"]["message"]

#     response_text = analyze_email(sender, content)

#     send_response_to_sber(user_id, response_text)

#     return jsonify({"status": "ok", "reply": response_text})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
