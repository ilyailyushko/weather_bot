import constant
from constant import tg_bot_token
from constant import owm_token
import telebot
from telebot import types
import pyowm

owm = pyowm.OWM(owm_token, language='ru')  # You MUST provide a valid API key
bot = telebot.TeleBot(tg_bot_token)


# Бот здоровается с юзером, при старте
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    bot.reply_to(message, "👋Привет, Напиши мне город или страну,"+
                          "а я расскажу про погоду на данный момент!")


# Бот Принимает название локации, проверяем есть ли такой город в апи OWM.
# Если Локация найдена - показываем погоду, если не найдена,
# - пишем 🤷‍♂️Увы, но Я не смог найти [сообщение юзера]
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    try:
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']
        wind = w.get_wind()['speed']
        hum = w.get_humidity()
        answer = '👇 ' + message.text + ' 👇' + '\n\n'
        answer += '📍____➡️ ' + w.get_detailed_status() + '\n\n'
        answer += '🌡____➡️ ' + str(round(temp)) + ' ℃' + '\n\n'
        answer += '🚰____➡️ ' + str(round(hum)) + ' %' + '\n\n'
        answer += '🌬___ ➡️ ' + str(wind) + ' М.С' + '\n\n'

        # добавляем кнопку
        # клавиатура
        markup = types.ReplyKeyboardMarkup(True, True)
        btn = message.text
        markup.row(btn)

        bot.reply_to(message, answer, reply_markup=markup)
    except:
        bot.reply_to(message, '🤷‍♂️Увы, но Я не смог найти '+ message.text)

bot.polling(none_stop=True)