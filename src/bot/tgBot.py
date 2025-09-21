from botComands import *
import telebot
from transliterate import translit, get_available_language_codes
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def start_command_message(message):
    markup = start_command()
    bot.send_message(message.chat.id, "Что вы хотите узнать сегодня?", reply_markup=markup)

@bot.callback_query_handler(func=lambda callback:True)
def callback_commands(callback):
    if callback.data == 'currency':
        currency_result = cur()
        bot.send_message(callback.message.chat.id, "Вот актуальный курс валют на сегодня \n\n" f"{currency_result}")

    if callback.data == 'weather':
        bot.send_message(callback.message.chat.id, "Напишите город в котором хотите узнать погоду")

        @bot.message_handler(content_types=['text'])
        def get_weather_link(message):
            city = message.text.strip().lower()
            city_cir = translit(city, reversed=True)
            link = "https://pogoda.mail.ru/prognoz/" + city_cir + "/"

            pos = requests.get(link)
            soup = BeautifulSoup(pos.text, "html.parser")
            weather = soup.find("div", class_='e487206871 dedbbf63df bfbd3eb239')

            remake_city = city[:-1]
            if city[-1:] == "ы":
                remake_city += "ах"
            elif city[-1:] != "ы":
                remake_city += "е"

            bot.send_message(message.chat.id, "Сегодня в " + remake_city.title() + f" {weather.text.strip()}")
            

@bot.message_handler(commands=['currency'])
def currency_command(message):
    currency_result = cur()
    bot.send_message(message.chat.id, "Вот актуальный курс валют на сегодня \n\n" f"{currency_result}")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()