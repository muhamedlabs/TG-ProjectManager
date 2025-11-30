import telebot
import logging
import threading
import schedule
import time
from admin.config import TOKEN

from commands.start_handlers import handle_start, handle_support, handle_commands, handle_advertise, handle_message
from commands.app_wallpaper import dispatch_random_wallpaper
from commands.app_music import play_random_music
from commands.Isanasume.app_isana_resume import all_resume
from commands.Isanasume.app_groups import gro_gamequest_news, gro_nanson_cfm, gro_andremuhamedd
from commands.mailing import mall_broadcast

logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(TOKEN)


# ---------- ОБРАБОТЧИКИ КОМАНД ----------

@bot.message_handler(commands=['start'])
def cmd_start(message):
    handle_start(bot, message)


@bot.message_handler(func=lambda m: m.text == "Финансовая поддержка проектов")
def cmd_support(message):
    handle_support(bot, message)


@bot.message_handler(func=lambda m: m.text == "Команды бота")
def cmd_commands(message):
    handle_commands(bot, message)


@bot.message_handler(func=lambda m: m.text == "Приобрести рекламу")
def cmd_advertise(message):
    handle_advertise(bot, message)


# Универсальный обработчик пользовательских сообщений
@bot.message_handler(func=lambda m: m.text and not any(
    word in m.text.lower()
    for word in [
        "финансовая поддержка", "приобрести рекламу", "команды бота",
        "поддержка", "newsletter", "wallpaper", "resume", "music",
        "start", "nanson_cfm", "gamequest_news", "andremuhamedd"
    ]
))
def msg_user_input(message):
    handle_message(bot, message)


@bot.message_handler(commands=['music'])
def cmd_music(message):
    play_random_music(bot, message, r'commands/myzis')


@bot.message_handler(commands=['wallpaper'])
def cmd_wallpaper(message):
    dispatch_random_wallpaper(bot, message, r'commands/wallpaper')


@bot.message_handler(commands=['resume'])
def cmd_resume(message):
    all_resume(bot, message, r'commands/Isanasume/Resume Muhamed.pdf')


@bot.message_handler(commands=['gamequest_news'])
def cmd_gamequest(message):
    gro_gamequest_news(bot, message)


@bot.message_handler(commands=['nanson_cfm'])
def cmd_nanson(message):
    gro_nanson_cfm(bot, message)


@bot.message_handler(commands=['andremuhamedd'])
def cmd_andre(message):
    gro_andremuhamedd(bot, message)


@bot.message_handler(commands=['newsletter'])
def cmd_mailing(message):
    mall_broadcast(bot, message)


# ---------- ЗАПУСК БОТА ----------

def start_bot():
    logging.info("Бот запущен и прокладывает путь проектам Андрея Мухамеда ✨")
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=125)
        except telebot.apihelper.ApiTelegramException as e:
            if e.result.status_code == 429:
                retry_after = int(e.result.json()['parameters']['retry_after'])
                time.sleep(retry_after)
            elif e.result.status_code == 502:
                time.sleep(5)
            else:
                logging.error(f"ApiTelegramException: {e}")
                time.sleep(25)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(25)


# ---------- ПЛАНИРОВЩИК ----------

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


# ---------- RATE LIMIT ----------

LAST_REQUEST_TIME = 0
REQUEST_INTERVAL = 1


def rate_limited_request(func):
    def wrapper(*args, **kwargs):
        global LAST_REQUEST_TIME
        now = time.time()
        if now - LAST_REQUEST_TIME < REQUEST_INTERVAL:
            time.sleep(REQUEST_INTERVAL - (now - LAST_REQUEST_TIME))
        LAST_REQUEST_TIME = time.time()
        return func(*args, **kwargs)
    return wrapper


@rate_limited_request
def safe_send(chat_id, text):
    bot.send_message(chat_id, text)


# ---------- MAIN ----------

if __name__ == "__main__":
    bot_thread = threading.Thread(target=start_bot)
    sched_thread = threading.Thread(target=run_scheduler)

    bot_thread.start()
    sched_thread.start()

    bot_thread.join()
    sched_thread.join()
