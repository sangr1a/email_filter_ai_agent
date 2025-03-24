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
    content = " ".join(line.strip() for line in lines[4:])
    return subject, sender, content

# Функция для анализа важности письма
def analyze_email(subject: str, sender: str, content: str):
    """Анализирует письмо и маркирует его в зависимости от отправителя и триггерных слов."""
    sender_boss = sender in BOSSES
    trigger_word = any(word in content.lower() for word in TRIGGER_WORDS)
    
    # Определение типа письма
    if sender_boss and trigger_word:
        label = "mail_boss_and_trigger"
        prompt_text = "Ты системный инженер. Тебе пришло уведомление от важного человека (начальника или иной высокой должности) о сбое в системе. С учетом известных случаев подобных сбоев составь пользователю план действий по решению проблемы. Ответ должен быть адресован пользователю, а ответ должен начинаться и писаться в духе персонажа Сберкот"
    elif sender_boss:
        label = "mail_boss"
        prompt_text = "Тебе пришло письмо от важного человека (начальника или иной высокой должности). Внимательно изучи письмо и напиши краткое изложение. Предложи пользователю варианты ответа в таком формате: answer_1[текст]...answer_2[текст]"
    elif trigger_word:
        label = "mail_trigger"
        prompt_text = "Ты системный инженер. Тебе пришло уведомление о сбое в системе, предложи пользователю несколько вариантов решения проблемы.  Ответ должен быть адресован пользователю, а ответ должен начинаться и писаться в духе персонажа Сберкот."
    else:
        label = "mail_simple"
        prompt_text = ""
    
    if prompt_text:
        response = giga([HumanMessage(content=prompt_text)])
        return f"Маркировка: {label}\nОтвет GigaChat: {response.content}"
    else:
        return f"Маркировка: {label} (Нет необходимости в ответе)"
