import telebot
from API import get_weather
from dotenv import load_dotenv
import os, json
load_dotenv()

token = os.getenv('token')
bot = telebot.TeleBot(token)

with open('f.json', 'r', encoding='utf-8') as file:
    users = json.load(file)


@bot.message_handler(commands=['start'])
def start(message):
    hello = 'Добрый день, я ваш персональный метеоролог.'
    bot.send_message(message.chat.id, text=hello)
    str_id = str(message.chat.id)
    if str(str_id) not in users:
        change_city(message)
    else:
        print(users[str_id])
    

def change_city(message):
    bot.send_message(message.chat.id, text='Укажите название города')
    bot.register_next_step_handler(message, save_city)

def save_city(message):
    users[str(message.chat.id)] = message.text
    with open('f.json', 'w', encoding='utf-8') as file:
        json.dump(users, file, ensure_ascii=False)
        print(users)
    bot.send_message(message.chat.id, text=f'Город {message.text} успешно сохранен!', reply_markup=lobby())
    

def lobby():
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=False)
    button1 = telebot.types.KeyboardButton('Текущая погода')
    button2 = telebot.types.KeyboardButton('Подробный прогноз на дату')
    button3 = telebot.types.KeyboardButton('Сменить город')
    keyboard.add(button1, button2, button3)
    return keyboard

def current_message(message):
    try:
        weather = get_weather(users[str(message.chat.id)])
        answer = '\n'.join(weather)
    except:
        answer = 'Погода по данному городу не найдена'
    bot.send_message(message.chat.id, text=answer)

@bot.message_handler(content_types=['text'])
def check_message(message):
    if message.text == 'Текущая погода':
        current_message(message)
    elif message.text == 'Сменить город':
        change_city(message)
    elif message.text == 'Подробный прогноз на дату':
        bot.send_message(message.chat.id, text='Кнопка в разработке...')
    else:
        bot.send_message(message.chat.id, text='Я вас не понимать')

bot.polling()

