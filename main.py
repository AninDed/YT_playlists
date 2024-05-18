import util
import telebot

bot = telebot.TeleBot(util.BOT_TOKEN)


@bot.message_handler(commands=['run'])
def test(message):
    msgs = util.all_way()
    bot.send_message(chat_id=util.CHAT_IDS['games'],
                     text=msgs['games'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)

    bot.send_message(chat_id=util.CHAT_IDS['enter'],
                     text=msgs['enter'],
                     parse_mode='HTML',
                     disable_web_page_preview=True)


bot.infinity_polling(timeout=10, long_polling_timeout=5)
