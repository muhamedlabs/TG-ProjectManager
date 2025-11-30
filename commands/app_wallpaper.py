# app_wallpaper.py
import os
import random
import logging

# Функция для обработки команды /wallpaper
def dispatch_random_wallpaper(bot, message, wallpapers_folder_path):
    try:
        # Получаем список файлов в папке с изображениями
        image_files = os.listdir(wallpapers_folder_path)
        
        if not image_files:
            raise FileNotFoundError("Отсутствуют файлы с обоями")
        
        # Выбираем случайное изображение из списка
        random_image_file = random.choice(image_files)
        
        # Путь к выбранному изображению
        image_path = os.path.join(wallpapers_folder_path, random_image_file)
        
        # Отправляем изображение пользователю
        with open(image_path, 'rb') as image_file:
            bot.send_photo(message.chat.id, image_file)
    except Exception as e:
        logging.error(f"Ошибка при обработке команды /wallpaper: {e}, file: {random_image_file}")
        bot.reply_to(message, "Произошла ошибка при отправке обоев.")
