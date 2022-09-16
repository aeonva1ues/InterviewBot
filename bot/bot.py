from . import bot
import time


def run_bot():
    running = True
    print('[BOT] INTERVIEW BOT IS RUNNING')
    while running:
        try:
            bot.polling()
        except Exception as error:
            print(f'[ERROR] {error}')
            time.sleep(4)