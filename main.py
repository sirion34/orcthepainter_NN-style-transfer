import telebot
from telebot import types
import NN
import PIL

bot = telebot.TeleBot('5541199205:AAG8vGUcWuRVYnnPaz9YMDFbEeMf-vsuQ2Y')
imagesToLoad = []


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Ну, Здравствуй, <b>{message.from_user.first_name}</b>!' \
           f' Готов вкалывать... Если хочешь список команд, то введи /help'
    # {message.from_user.last_name}
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def start(message):
    mess = f'Я отличный художник! Я могу перенести стиль одной картинки на другую! ' \
           f'Для этого загрузи любое изображение, которое тебе хочется.'
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # photo_button = types.KeyboardButton('Загрузить фото')
    # markup.add(photo_button)
    bot.send_message(message.chat.id, mess, parse_mode='html')  # , reply_markup=markup)


@bot.message_handler(commands=['remove'])
def start(message):
    imagesToLoad.clear()
    mess = f'Загрузи нужное изображение.'
    bot.send_message(message.chat.id, mess, parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, "Ну, здравствуй!", parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Извините, я не понимаю о чем Вы говорите...", parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):

    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    root_folder =  # here is the address of the root folder 'C:/Users/...'
    src = root_folder + message.photo[1].file_id + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    imagesToLoad.append(src)
    if len(imagesToLoad) == 1:
        bot.reply_to(message, f'Фотография получена, загрузите какой стиль перенести, '
                              f'если хотите отменить, то напишите команду /remove.')
    if len(imagesToLoad) == 2:
        bot.reply_to(message, f'Стиль получен! Ладно, за работу!')
        respic = NN.make_image(imagesToLoad[0], imagesToLoad[1])
        bot.reply_to(message, f'Работа сделана!')
        imagesToLoad.clear()
        bot.send_photo(message.chat.id, photo=open(respic, 'rb'))


bot.polling(none_stop=True)
