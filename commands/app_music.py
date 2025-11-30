# app_music.py
import os
import random
import logging

# Функция для обработки команды /music
def play_random_music(bot, message, music_folder_path):
    try:
        # Получаем список файлов в папке с музыкой
        music_files = os.listdir(music_folder_path)
        
        if not music_files:
            raise FileNotFoundError("Отсутствуют файлы с музыкой")
        
        # Выбираем случайный файл из списка
        random_music_file = random.choice(music_files)
        
        # Путь к выбранному файлу
        file_path = os.path.join(music_folder_path, random_music_file)
        
        # Отправляем аудиофайл пользователю
        with open(file_path, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
    
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /music: {e}")
        bot.reply_to(message, "Произошла ошибка при отправке музыки.")

