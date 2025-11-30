import logging
import schedule
from telebot import types
import os
import threading
import time

USER_DATA_FILE = r'admin/user_data.txt'


# -----------------------------
# /start
# -----------------------------
def handle_start(bot, message):
    user_id = message.from_user.id
    username = message.from_user.username
    user_link = f"https://t.me/{username}" if username else None

    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    chat_id = message.chat.id

    # Создаём файл, если нет
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            pass

    # Читаем существующих пользователей
    with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
        existing_users = f.readlines()
        existing_user_ids = [
            line.split(',')[0].split(': ')[1].strip() for line in existing_users if line.strip()
        ]

    # Записываем новые данные
    if str(user_id) not in existing_user_ids:
        with open(USER_DATA_FILE, 'a', encoding='utf-8') as f:
            f.write(
                f"ID пользователя: {user_id}, Имя пользователя: {username}, "
                f"Имя: {first_name}, Фамилия: {last_name}, Ссылка: {user_link}, ID чата: {chat_id}\n"
            )

    welcome_text = (
        f"👋 Привет, {first_name}! Я бот-менеджер Андрея Мухамеда. "
        f"Моя цель — сделать твой опыт максимально удобным. "
        f"Используй кнопки ниже, чтобы узнать доступные команды."
    )

    # Картинка приветствия
    try:
        with open(r'admin/Filemania/Gallery/Greetings.jpg', 'rb') as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=welcome_text,
                reply_markup=get_main_keyboard()
            )
    except Exception as e:
        logging.error(f"Ошибка отправки приветственного изображения: {e}")


# -----------------------------
# Отправка ежемесячных напоминаний всем пользователям
# -----------------------------
def monthly_reminder(bot):
    if not os.path.exists(USER_DATA_FILE):
        return

    with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        parts = line.split(',')
        chat_part = [p for p in parts if "ID чата:" in p]

        if not chat_part:
            continue

        chat_id = chat_part[0].split(':')[1].strip()

        try:
            send_reminder(bot, chat_id)
        except Exception as e:
            logging.error(f"Ошибка отправки напоминания пользователю {chat_id}: {e}")


# -----------------------------
# Напоминание
# -----------------------------
def send_reminder(bot, chat_id):
    video_path = r'admin/Filemania/Video/2024-project.mp4'
    caption_message = (
        "Привет! Не забыл ли ты о наших проектах?\n\n"
        "Если хочешь ознакомиться с проектами на YouTube — переходи сюда: https://bit.ly/4cZEipJ"
    )

    text_message = (
        "Твоя поддержка помогает нам расти и создавать качественный контент!"
    )

    try:
        with open(video_path, 'rb') as video:
            bot.send_video(
                chat_id,
                video,
                caption=caption_message,
                parse_mode='Markdown'
            )

        bot.send_message(chat_id, text_message)

    except Exception as e:
        logging.error(f"Ошибка отправки напоминания: {e}")


# -----------------------------
# Клавиатура
# -----------------------------
def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    keyboard.add(
        types.KeyboardButton("Команды бота"),
        types.KeyboardButton("Приобрести рекламу"),
        types.KeyboardButton("Финансовая поддержка проектов")
    )

    return keyboard


# -----------------------------
# Финансовая поддержка
# -----------------------------
def handle_support(bot, message):
    support_text = (
        "💵 Ваш вклад помогает нам развивать проекты.\n\n"
        "Donationalerts: https://www.donationalerts.com/r/andremuhamad\n"
        "Patreon: https://www.patreon.com/andremuhamad"
    )

    bot.send_message(message.chat.id, support_text, parse_mode="Markdown")


# -----------------------------
# Команды
# -----------------------------
def handle_commands(bot, message):
    bot.send_message(
        message.chat.id,
        "🛠️ Все команды:\n"
        "/start — Перезапуск\n"
        "/nanson_cfm — Музыка Nanson\n"
        "/music — Случайная музыка\n"
        "/gamequest_news — Игровые новости\n"
        "/wallpaper — Обои Game Quest\n"
        "/andremuhamedd — Личный канал\n"
        "/resume — Резюме Андрея Мухамеда"
    )


# -----------------------------
# Реклама
# -----------------------------
def handle_advertise(bot, message):
    bot.send_message(
        message.chat.id,
        "🛍️ Для заказа рекламы:\n"
        "Email: akynsasa@gmail.com\n"
        "Telegram: https://t.me/admirall_times\n\n"
        "Мы подберём формат, который идеально подойдёт для вашего проекта."
    )


# -----------------------------
# Ответ на обычные сообщения
# -----------------------------
def handle_message(bot, message):
    bot.send_message(
        message.chat.id,
        "🤖 Бот сейчас занят работой над проектами Андрея Мухамеда. "
        "Рекомендуем подписаться на наш канал: https://t.me/andremuhamedd"
    )


# -----------------------------
# Запуск планировщика в отдельном потоке
# -----------------------------
def start_scheduler(bot):
    schedule.every().month.do(lambda: monthly_reminder(bot))

    def schedule_runner():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=schedule_runner, daemon=True).start()
