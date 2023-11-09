import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler, CallbackContext
import time

TELEGRAM_BOT_TOKEN = '6144521848:AAGozRb6CeCRacrld6vjoZM-rb6fXuikN8I'
TELEGRAM_CHAT_ID = '446995765'
url = "https://m.cheelee.io/"

def start(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Бот начал мониторинг rare очков. Используйте /stop для остановки.")

def stop(update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Бот остановлен.")
    context.job_queue.stop()

def check_rare_points(context: CallbackContext):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rare_points = soup.find_all("label", class_="btn btn--rare ng-star-inserted")

        if rare_points:
            message = "Rare очки появились!"
            context.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
            context.job_queue.stop()
        else:
            print("Нет изменений в rare очках.")
    else:
        print(f"Ошибка {response.status_code}. Невозможно получить доступ к странице.")

def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("stop", stop))

    # Проверка каждые 60 секунд
    updater.job_queue.run_repeating(check_rare_points, interval=60, first=0)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()



