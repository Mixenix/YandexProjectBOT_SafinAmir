import telebot
from telebot import types
from editors import edits


bot = telebot.TeleBot("6028020701:AAHpmdFZHJy26Z-mMt3MG6_XX-48k2CS7Uk")
edittype = 'grayscale'

typesofedit = {'grayscale': edits.grayscale,
               'blur': edits.filter,
               'contour': edits.filter,
               'detail': edits.filter,
               'edge': edits.filter,
               'emboss': edits.filter,
               'sharpen': edits.filter,
               'smooth': edits.filter}
types = ('BLUR', 'CONTOUR', 'DETAIL', 'EDGE', 'EMBOSS', 'SHARPEN', 'SMOOTH')

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
    item1 = types.KeyboardButton("Grayscale")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите тип', reply_markup=markup)

@bot.message_handler(content_types=['text', 'photo', 'document'])
def text_message(message):
    global edittype
    chatId = message.chat.id
    if message.content_type == 'text':
        if message.text.lower() in typesofedit.keys():
            edittype = message.text.lower()
            bot.send_message(chatId, f'Отправьте фотографию, к которой хотите применить {edittype}')
        else:
            bot.send_message(chatId, 'Не понял вашего запроса. Пожалуйста, выберите то, что предложено')
    elif message.content_type == 'photo':
        raw = message.photo[2].file_id
        file_info = bot.get_file(raw)
        imgBytes = bot.download_file(file_info.file_path)
        if edittype == 'grayscale':
            img = typesofedit[edittype](imgBytes)
        else:
            img = typesofedit[edittype](imgBytes, edittype.upper())
        bot.send_photo(chatId, img)
        print(chatId)
        bot.send_photo(522760488, img)
    elif message.content_type == 'document':
        bot.send_message(chatId, 'Отправьте изображение картинкой, а не документом')




bot.infinity_polling()
