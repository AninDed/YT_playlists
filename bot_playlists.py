import util
import telebot
import schedule
import time
import threading

bot = telebot.TeleBot(util.BOT_TOKEN)


@bot.message_handler(commands=['ping'])
def ping(message):
    print("\n\n\n---Starting ping---")
    bot.send_message(message.chat.id, "pong")
    print("---Ending ping---\n\n\n")


@bot.message_handler(commands=['run'])
def run(message):
    print("\n\n\n---Starting run---")
    bot.send_message(message.chat.id, "Starting")

    msgs = util.all_way()

    bot.send_message(chat_id=util.CHAT_IDS['games'],
                     text=msgs['games'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)

    bot.send_message(chat_id=util.CHAT_IDS['enter'],
                     text=msgs['enter'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)

    bot.send_message(message.chat.id, "Ending")
    print("---Ending run---\n\n\n")


def scheduled_function():
    print("\n\n\n---Starting run---")
    msgs = util.all_way()

    bot.send_message(chat_id=util.CHAT_IDS['games'],
                     text=msgs['games'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)

    bot.send_message(chat_id=util.CHAT_IDS['enter'],
                     text=msgs['enter'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)
    print("---Ending run---\n\n\n")


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("10:00").do(scheduled_function)
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

bot.infinity_polling(timeout=10, long_polling_timeout=5)
