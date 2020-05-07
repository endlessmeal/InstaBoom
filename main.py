from instapy import InstaPy
from selenium import webdriver
import telebot
import constants

bot = telebot.TeleBot(constants.token)
login = constants.login
password = constants.password
selectedOption = ''
like_tag = ''
option_name = ''

@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Лайк', 'Комментарий')
    user_markup.row('Подписка', '/start')
    bot.send_message(message.from_user.id, 'Привет, выбери что бот должен делать', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'лайк':
        global option_name
        option_name = 'хештег'
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'комментарий':
        global option_name
        option_name = 'комментарий'
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'подписка':
        global option_name
        option_name = 'количество'
        bot.send_message(message.from_user.id, selected(message))


def selected(message):
    global selectedOption
    bot.send_message(message.from_user.id, 'Вы выбрали ' + message.text + '\n' + 'Введите Логин')
    selectedOption = message.text
    bot.register_next_step_handler(message, get_login)


print(selectedOption)


def get_login(message):
    global login
    login = message.text
    bot.send_message(message.from_user.id, 'Введите пароль')
    bot.register_next_step_handler(message, get_password)


def get_password(message):
    global password
    password = message.text
    bot.send_message(message.from_user.id, 'Авторизация, подождите')
    authorization(message)


def authorization(message):
    print(login)
    print(password)
    print(message.text)
    global session
    session = InstaPy(username=str(login), password=str(password), want_check_browser=False, headless_browser=True)
    if session.login():
        bot.send_message(message.from_user.id, 'Успешно' + '\n' + 'Введите ' + option_name)
        bot.register_next_step_handler(message, choice)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так')
        bot.register_next_step_handler(message, get_login)


def choice(message):
    global like_tag
    like_tag = message.text
    print(like_tag)
    if selectedOption.lower() == 'лайк':
        bot.send_message(message.from_user.id, 'Бот ставит 30 лайков в час по хештегу: ' + str(like_tag))
        session.set_quota_supervisor(enabled=True, peak_likes_hourly=30, peak_likes_daily=800)
        session.like_by_tags([str(like_tag)], amount=10000)


bot.polling(none_stop=True)

#
# session.like_by_tags(["style", "look"], amount=5)
