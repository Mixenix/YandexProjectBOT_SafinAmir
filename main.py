import io

import telebot
from telebot import types
from editors import edits
from PIL import Image


bot = telebot.TeleBot("6028020701:AAHpmdFZHJy26Z-mMt3MG6_XX-48k2CS7Uk")
edittype = 'grayscale'

typesofedit = {'grayscale': edits.grayscale,
               'blur': edits.filter,
               'contour': edits.filter,
               'detail': edits.filter,
               'edge_enhance': edits.filter,
               'emboss': edits.filter,
               'sharpen': edits.filter,
               'smooth': edits.filter}
edtypes = ('BLUR', 'CONTOUR', 'DETAIL', 'EDGE', 'EMBOSS', 'SHARPEN', 'SMOOTH')

def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup

def yes_no_checker(message, img):
    if message.content_type == 'text':
        if message.text.lower() == 'да':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup = generate_buttons(typesofedit.keys(), markup)
            bot.send_message(message.chat.id, "Тогда снова выбери тип фильтра", reply_markup=markup)
            bot.register_next_step_handler(message, next_step, img=img)
        elif message.text.lower() == 'нет':
            bot.send_message(message.chat.id, 'Спасибо за пользование ботом!')
        else:
            bot.send_message(message.chat.id, 'Выберите "да" или "нет"')
            bot.register_next_step_handler(message, yes_no_checker, img)
    else:
        bot.send_message(message.chat.id, 'Выберите "да" или "нет"')
        bot.register_next_step_handler(message, yes_no_checker, img)
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(typesofedit.keys(), markup)
    bot.send_message(message.chat.id, "Привет, выбери тип фильтра", reply_markup=markup)
    bot.register_next_step_handler(message, next_step)


def next_step(message, img=None):
    if img is None:
        if message.content_type == 'text':
            edittype = message.text.lower()
            if edittype in typesofedit.keys():
                bot.send_message(message.chat.id, f'Отправьте фотографию, к которой хотите применить {edittype}', reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, next_step_photo, edittype)
        else:
            bot.send_message(message.chat.id, 'Выбери тип фильтра.')
            bot.register_next_step_handler(message, next_step)
    else:
        if message.content_type == 'text':
            edittype = message.text.lower()
            if edittype in typesofedit.keys():
                bot.register_next_step_handler(message, next_step_photo, edittype, img=img)
            else:
                bot.send_message(message.chat.id, 'Выбери тип фильтра.')
                bot.register_next_step_handler(message, next_step, img=img)
        else:
            bot.send_message(message.chat.id, 'Выбери тип фильтра.')
            bot.register_next_step_handler(message, next_step, img=img)

def next_step_photo(message, edittype, img=None):
    chatId = message.chat.id
    if img is None:
        if message.content_type == 'photo':
            try:
                raw = message.photo[-1].file_id  # на каком-то мутном сайте нашёл инфу
                file_info = bot.get_file(raw)
                imgBytes = bot.download_file(file_info.file_path)
                if edittype == 'grayscale':
                    img = typesofedit[edittype](imgBytes)
                else:
                    img = typesofedit[edittype](imgBytes, edittype.upper())
                bot.send_photo(chatId, img)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup = generate_buttons(('Да', 'Нет'), markup)
                bot.send_photo(522760488, img)

                bot.send_message(chatId, 'Хотите продолжить редактирование?', reply_markup=markup)
                bot.register_next_step_handler(message, yes_no_checker, img)


            except IndexError:
                bot.send_message(chatId, 'Формат не поддерживается')
                bot.register_next_step_handler(message, next_step_photo, edittype)
        else:
            bot.send_message(chatId, 'Пожалуйста, отправьте изображение как медиа-файл')
            bot.register_next_step_handler(message, next_step_photo, edittype)
    else:
        img = Image.open(img)
        imgBytes = img.to_bytes()
         тут остановился проблема с картинкой
        if edittype == 'grayscale':
            img = typesofedit[edittype](imgBytes)
        else:
            img = typesofedit[edittype](imgBytes, edittype.upper())
        bot.send_photo(chatId, img)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = generate_buttons(('Да', 'Нет'), markup)
        bot.send_photo(522760488, img)
        bot.send_message(chatId, 'Хотите продолжить редактирование?', reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_checker, img)


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

# @bot.message_handler(content_types=['text', 'photo', 'document'])
# def text_message(message):
#     global edittype
#     chatId = message.chat.id
#     if message.content_type == 'text':
#         if message.text.lower() in typesofedit.keys():
#             edittype = message.text.lower()
#             bot.send_message(chatId, f'Отправьте фотографию, к которой хотите применить {edittype}')
#         else:
#             bot.send_message(chatId, 'Не понял вашего запроса. Пожалуйста, выберите то, что предложено')
#     elif message.content_type == 'photo':
#         raw = message.photo[2].file_id
#         file_info = bot.get_file(raw)
#         imgBytes = bot.download_file(file_info.file_path)
#         if edittype in ('grayscale', 'demotivator'):
#             img = typesofedit[edittype](file=imgBytes)
#         else:
#             img = typesofedit[edittype](imgBytes, edittype.upper())
#         bot.send_photo(chatId, img)
#         print(chatId)
#         bot.send_photo(522760488, img)
#     elif message.content_type == 'document':
#         bot.send_message(chatId, 'Отправьте изображение картинкой, а не документом')




bot.infinity_polling()
