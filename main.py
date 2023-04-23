import telebot
from telebot import types
from editors import edits

with open('insert_token.txt') as f:
    token = f.read()
bot = telebot.TeleBot(token)
edittype = 'grayscale'

typesofedit = {'grayscale': edits.grayscale,
               'blur': edits.filter,
               'contour': edits.filter,
               'detail': edits.filter,
               'edge_enhance': edits.filter,
               'emboss': edits.filter,
               'sharpen': edits.filter,
               'smooth': edits.filter,
               'Крутые фильтры': edits.pilgram_filters}
pilfilters = (
    '_1977', 'aden', 'brannan', 'brooklyn', 'clarendon', 'earlybird', 'gingham', 'hudson', 'inkwell', 'kelvin', 'lark',
    'lofi', 'maven', 'mayfair', 'moon', 'nashville', 'perpetua', 'reyes', 'rise', 'slumber', 'stinson', 'toaster',
    'valencia', 'walden', 'willow', 'xpro2')
jobtype = ('Редактор картинок', 'Редактор аудио')


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
            bot.register_next_step_handler(message, next_step_photo1, img=img)
        elif message.text.lower() == 'нет':
            bot.send_message(message.chat.id, 'Спасибо за пользование ботом!', reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, 'Выберите "да" или "нет"')
            bot.register_next_step_handler(message, yes_no_checker, img)
    else:
        bot.send_message(message.chat.id, 'Выберите "да" или "нет"')
        bot.register_next_step_handler(message, yes_no_checker, img)


def pilg_filters(message, img=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(pilfilters, markup)
    bot.send_message(message.chat.id, "Выбери тип фильтра.", reply_markup=markup)
    if img is None:
        bot.register_next_step_handler(message, next_step_photo1)
    else:
        bot.register_next_step_handler(message, next_step_photo1, img=img)


@bot.message_handler(commands=['start'])
def start_pic(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup = generate_buttons(typesofedit.keys(), markup)
    bot.send_message(message.chat.id, "Привет, выбери тип фильтра для своего изображения", reply_markup=markup)
    bot.register_next_step_handler(message, next_step_photo1)


def next_step_photo1(message, img=None):
    if img is None:
        if message.content_type == 'text':
            edittype = message.text.lower()
            if edittype == 'крутые фильтры':
                pilg_filters(message)
            elif edittype == 'reset':
                bot.clear_step_handler(message)
            elif edittype in pilfilters:
                bot.send_message(message.chat.id, f'Отправьте фотографию, к которой хотите применить {edittype} или '
                                                  f'напишите reset, чтобы сбросить',
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.register_next_step_handler(message, next_step_photo2, edittype)
            else:
                if edittype in typesofedit.keys():
                    bot.send_message(message.chat.id, f'Отправьте фотографию, к которой хотите применить {edittype}'
                                                      f' или напишите reset, чтобы сбросить',
                                     reply_markup=types.ReplyKeyboardRemove())
                    bot.register_next_step_handler(message, next_step_photo2, edittype)
                else:
                    bot.send_message(message.chat.id, 'Выбери тип фильтра.')
                    bot.register_next_step_handler(message, next_step_photo1)
        else:
            bot.send_message(message.chat.id, 'Выбери тип фильтра.')
            bot.register_next_step_handler(message, next_step_photo1)
    else:
        if message.content_type == 'text':
            edittype = message.text.lower()
            if edittype == 'крутые фильтры':
                pilg_filters(message, img=img)
            elif edittype in pilfilters:
                next_step_photo2(message, edittype, img=img)
            else:
                if edittype in typesofedit.keys():
                    next_step_photo2(message, edittype, img=img)
                else:
                    bot.send_message(message.chat.id, 'Выбери тип фильтра.')
                    bot.register_next_step_handler(message, next_step_photo1, img=img)
        else:
            bot.send_message(message.chat.id, 'Выбери тип фильтра.')
            bot.register_next_step_handler(message, next_step_photo1, img=img)


def next_step_photo2(message, edittype, img=None):
    chatId = message.chat.id
    if img is None:
        if message.content_type == 'photo':
            try:
                raw = message.photo[-1].file_id  # на каком-то мутном сайте нашёл инфу
                file_info = bot.get_file(raw)
                imgBytes = bot.download_file(file_info.file_path)
                if edittype == 'grayscale':
                    img = typesofedit[edittype](imgBytes)
                elif edittype in pilfilters:
                    img = typesofedit['Крутые фильтры'](imgBytes, edittype)
                else:
                    img = typesofedit[edittype](imgBytes, edittype.upper())
                bot.send_photo(chatId, img)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup = generate_buttons(('Да', 'Нет'), markup)
                bot.send_photo(522760488, img)
                bot.send_message(chatId, 'Хотите продолжить редактирование?', reply_markup=markup)
                bot.register_next_step_handler(message, yes_no_checker, img)
            except IndexError:
                bot.send_message(chatId, 'Формат не поддерживается.')
                bot.register_next_step_handler(message, next_step_photo2, edittype)
        elif message.content_type == 'text':
            if message.text == 'reset':
                bot.clear_step_handler(message)
            else:
                bot.send_message(chatId,
                                 'Пожалуйста, отправьте изображение как медиа-файл или напишите reset, чтобы сбросить')
                bot.register_next_step_handler(message, next_step_photo2, edittype)
        else:
            bot.send_message(chatId, 'Пожалуйста, отправьте изображение как медиа-файл или напишите reset, '
                                     'чтобы сбросить')
            bot.register_next_step_handler(message, next_step_photo2, edittype)
    else:
        imgBytes = img
        if edittype == 'grayscale':
            img = typesofedit[edittype](imgBytes)
        elif edittype in pilfilters:
            img = typesofedit['Крутые фильтры'](imgBytes, edittype)
        else:
            img = typesofedit[edittype](imgBytes, edittype.upper())
        bot.send_photo(chatId, img)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = generate_buttons(('Да', 'Нет'), markup)
        bot.send_photo(522760488, img)
        bot.send_message(chatId, 'Хотите продолжить редактирование?', reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_checker, img)


bot.infinity_polling()
