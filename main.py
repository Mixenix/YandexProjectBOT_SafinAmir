import telebot
from telebot import types

bot = telebot.TeleBot("6028020701:AAHpmdFZHJy26Z-mMt3MG6_XX-48k2CS7Uk")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет")


# @bot.message_handler(commands=['button'])
# def button_message(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Тип")
#     markup.add(item1)
#     bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Monochrome")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите тип', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_message(message):
    if message == 'Monochrome':

bot.infinity_polling()
