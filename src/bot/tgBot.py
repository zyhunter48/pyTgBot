from botComands import *
import telebot

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def start_command_message(message):
    markup = start_command()
    bot.send_message(message.chat.id, "Что вы хотите узнать сегодня?", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def currency_comand(callback):
    if callback.data == 'currency':
        currency_result = cur()
        bot.send_message(callback.message.chat.id, "Вот актуальный курс валют на сегодня \n\n" f"{currency_result}")
        print("Кнопка currency нажата")
        print(f"Результат функции cur(): {currency_result}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()