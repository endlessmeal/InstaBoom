from instapy import InstaPy
from selenium import webdriver
import telebot
import constants

bot = telebot.TeleBot(constants.token)
login = constants.login
password = constants.password


@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Лайк', 'Комментарий')
    user_markup.row('Подписка', '/start')
    bot.send_message(message.from_user.id, 'Привет, выбери что бот должен делать', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'лайк':
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'комментарий':
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'подписка':
        bot.send_message(message.from_user.id, selected(message))


def selected(message):
    bot.send_message(message.from_user.id, 'Вы выбрали ' + message.text + '\n' + 'Введите Логин')
    bot.register_next_step_handler(message, get_login)


def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'Введи пароль')
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global password
    password = message.text
    bot.send_message(message.from_user.id, 'Авторизация, подождите')
    bot.register_next_step_handler(message, authorization(message))


def authorization(message):
    print(login)
    print(password)
    session = InstaPy(username=str(login), password=str(password), want_check_browser=False, headless_browser=False)
    if session.login() == 'SUCCESS':
        bot.send_message(message.from_user.id, 'Успешно')
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так')


bot.polling(none_stop=True)

#
# session.like_by_tags(["style", "look"], amount=5)
