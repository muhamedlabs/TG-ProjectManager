# app_isana_resume.py
import logging

# Функция для обработки команды /resume
def all_resume(bot, message, resume_file_path):
    try:
        # Открываем PDF файл для чтения в бинарном режиме
        with open(resume_file_path, 'rb') as pdf_file:
            # Отправляем PDF файл пользователю
            bot.send_document(message.chat.id, pdf_file)
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /resume: {e}, файл: {resume_file_path}")
        bot.reply_to(message, "Произошла ошибка при отправке резюме.")
