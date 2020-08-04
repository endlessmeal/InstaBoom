from instapy import InstaPy
from selenium import webdriver
import telebot
import constants

bot = telebot.TeleBot(constants.token)
selectedOption = ''
value = ''
option_name = ''


@bot.message_handler(commands=['start'])
def start_message(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, True)
    user_markup.row('Лайк', 'Комментарий')
    user_markup.row('Подписка', '/start')
    bot.send_message(message.from_user.id, 'Привет, выбери что бот должен делать', reply_markup=user_markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    global option_name
    if message.text.lower() == 'лайк':
        option_name = 'хештег'
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'комментарий':
        option_name = 'комментарий'
        bot.send_message(message.from_user.id, selected(message))
    elif message.text.lower() == 'подписка':
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
    session.set_quota_supervisor(enabled=True, peak_likes_hourly=11, peak_likes_daily=800, peak_comments_daily=200,
                                 peak_comments_hourly=20, peak_follows_daily=200, peak_follows_hourly=15,
                                 sleep_after=["likes_d", "comments_d", "follows_d"], sleepyhead=True)
    if session.login():
        bot.send_message(message.from_user.id, 'Успешно' + '\n' + 'Введите ' + option_name)
        bot.register_next_step_handler(message, choice)
    else:
        bot.send_message(message.from_user.id, 'Что-то пошло не так')
        bot.register_next_step_handler(message, get_login)


def choice(message):
    global value
    value = message.text
    print(value)
    if selectedOption.lower() == 'лайк':
        bot.send_message(message.from_user.id, 'Бот ставит 30 лайков в час по хештегу: ' + str(value))
        session.like_by_tags([str(value)], amount=100)
    elif selectedOption.lower() == 'комментарий':
        bot.send_message(message.from_user.id, 'Бот пишет 20 комментариев в час: ' + str(value))
        session.set_do_comment(enabled=True, percentage=25)
        session.set_comments([str(value)])
    elif selectedOption.lower() == 'подписка':
        bot.send_message(message.from_user.id, 'Бот подписывается на 15 человек в час')
        session.set_do_follow(enabled=True, percentage=10, times=1000)


bot.polling(none_stop=True)
