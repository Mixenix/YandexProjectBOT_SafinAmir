# Редактор изображений в Telegram

Telegram-бот, применяющий фильтры к фотографиям. Умеет накладывать несколько фильтров последовательно — результат первого фильтра передается второму, и так далее.

## Функции

- 8 стандартных фильтров Pillow: grayscale, blur, contour, detail, edge_enhance, emboss, sharpen, smooth
- 26 фильтров из библиотеки Pilgram (Instagram-стиль): _1977, aden, brannan, brooklyn, clarendon, earlybird, gingham, hudson, inkwell, kelvin, lark, lofi, maven, mayfair, moon, nashville, perpetua, reyes, rise, slumber, stinson, toaster, valencia, walden, willow, xpro2
- Цепочки фильтров — можно применить несколько фильтров подряд к одному изображению
- Клавиатура с кнопками для выбора фильтров

## Стек

- **Python 3.8+**
- **pyTelegramBotAPI** — работа с Telegram API
- **Pillow** — обработка изображений
- **Pilgram** — Instagram-подобные фильтры
- **NumPy**, **SciPy** — вычислительная база под капотом

## Установка

```bash
pip install -r requirements.txt
```

Создайте файл `insert_token.txt` в корне проекта и запишите в него токен бота, полученный через @BotFather.

## Запуск

```bash
python main.py
```

В чате с ботом отправьте `/start` и следуйте инструкциям.

## Автор

Сафин Амир, проект в рамках Яндекс.Лицея (2023).
