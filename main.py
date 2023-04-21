import telebot
from telebot import types
from editors import edits
from editors.edits import Demotivator


bot = telebot.TeleBot("6028020701:AAHpmdFZHJy26Z-mMt3MG6_XX-48k2CS7Uk")
edittype = 'grayscale'

typesofedit = {'grayscale': edits.grayscale,
               'blur': edits.filter,
               'contour': edits.filter,
               'detail': edits.filter,
               'edge': edits.filter,
               'emboss': edits.filter,
               'sharpen': edits.filter,
               'smooth': edits.filter,
               'demotivator': Demotivator.create}
edtypes = ('BLUR', 'CONTOUR', 'DETAIL', 'EDGE', 'EMBOSS', 'SHARPEN', 'SMOOTH')

def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))

    return markup
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(typesofedit.keys(), markup)
    bot.send_message(message.chat.id, "Привет, выбери тип фильтра", reply_markup=markup)
    bot.register_next_step_handler(message, next_step)


def next_step(message):
    edittype = message.text.lower()
    if edittype in typesofedit.keys():
        bot.send_message(message.chat.id, f'Отправьте фотографию, к которой хотите применить {edittype}', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, next_step_photo, edittype)


def next_step_photo(message, edittype):
    chatId = message.chat.id
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        file_info = bot.get_file(raw)
        imgBytes = bot.download_file(file_info.file_path)
        if edittype in ('grayscale', 'demotivator'):
            img = typesofedit[edittype](file=imgBytes)
        else:
            img = typesofedit[edittype](imgBytes, edittype.upper())
        bot.send_photo(chatId, img)
        print(chatId)
        bot.send_photo(522760488, img)
    else:
        bot.send_message(chatId, 'Пожалуйста, отправьте изображение как медиа-файл')



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
