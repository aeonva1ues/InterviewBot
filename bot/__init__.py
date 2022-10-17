# Пакет, инициализирующий бота
import os

import telebot

TOKEN = os.getenv('TG_INTERVIEW_BOT_TOKEN')
# значение сохранено в переменной окружения для большей безопасности токена
bot = telebot.TeleBot(TOKEN)


from handlers.user_messages import start_message
