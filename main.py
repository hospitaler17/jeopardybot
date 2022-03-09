import datetime
import threading
import telebot
from aiogram import types


class Player:
    ID: int = 0
    name: str = 'Пустой слот '
    score: int = 0
    ready: bool = False


bot = telebot.TeleBot('[your-bot-code]')

counter = 0
master = Player()
master.name = ''

support = Player()
support.name = ''

player_1 = Player()
player_2 = Player()
player_3 = Player()
player_1.name += '1'
player_2.name += '2'
player_3.name += '3'


def buildButtons(message: types.Message):
    global master
    global player_1
    global player_2
    global player_3
    if master.name != '':
        bot.send_message(message.chat.id, 'Ваш ведущий: ' + master.name + '!')
    keyboard = telebot.types.ReplyKeyboardMarkup(False)
    button = telebot.types.KeyboardButton('Ответ готов!')
    keyboard.add(button)
    bot.send_message(message.chat.id, 'Ожидайте', reply_markup=keyboard)
    if player_1.ready & player_2.ready & player_3.ready:
        bot.send_message(master.ID, 'Все игроки готовы!')
        bot.send_message(player_1.ID, 'Игра начинается!')
        bot.send_message(player_2.ID, 'Игра начинается!')
        bot.send_message(player_3.ID, 'Игра начинается!')
        if support.ID != 0:
            bot.send_message(support.ID, 'Игра начинается!')


def buildSupportButtons(message: types.Message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    button_1 = ['200', '400']
    button_2 = ['600', '800']
    button_3 = ['Счет']
    button_4 = ['Новый вопрос']
    keyboard.add(*button_1)
    keyboard.add(*button_2)
    keyboard.add(*button_3)
    keyboard.add(*button_4)
    bot.send_message(message.chat.id, 'Выполнено!', reply_markup=keyboard)


######## Start GAME #########
@bot.message_handler(commands=["start"])
def start(message: types.Message):
    global player_1
    global player_2
    global player_3
    keyboard = telebot.types.ReplyKeyboardMarkup(True)
    # bot.send_message(message.chat.id, 'Выберите слот игрока!')
    if not player_1.ready:
        button_1 = telebot.types.KeyboardButton(player_1.name)
        keyboard.add(button_1)
    if not player_2.ready:
        button_2 = telebot.types.KeyboardButton(player_2.name)
        keyboard.add(button_2)
    if not player_3.ready:
        button_3 = telebot.types.KeyboardButton(player_3.name)
        keyboard.add(button_3)
    bot.send_message(message.chat.id, 'Выберите слот игрока!', reply_markup=keyboard)


@bot.message_handler(commands=["new"])
def new(message: types.Message):
    global counter
    if counter > 1:
        counter = 0
        print("==============================================")


@bot.message_handler(commands=["new_master"])
def new_master(message: types.Message):
    global master
    master.ID = message.chat.id
    master.name = message.chat.first_name
    bot.send_message(message.chat.id, master.name + ", Вы новый ведущий!")
    keyboard = telebot.types.ReplyKeyboardMarkup()
    button_1 = telebot.types.KeyboardButton('Новый вопрос')
    button_2 = telebot.types.KeyboardButton('Счет')
    keyboard.add(button_1)
    keyboard.add(button_2)
    bot.send_message(message.chat.id, message.text, reply_markup=keyboard)
    print("Новый ведущий: " + master.name)


@bot.message_handler(commands=["new_support"])
def new_support(message: types.Message):
    global support
    global master
    support.ID = message.chat.id
    support.name = message.chat.first_name
    print("Новый подручный: " + support.name)
    if master.ID != 0:
        bot.send_message(master.ID, 'Новый подручный: ' + support.name)
    buildSupportButtons(message)


##### GAME MENU #####
@bot.message_handler(content_types=['text'])
def ready(message: types.Message):
    global counter
    global master
    global support
    global player_1
    global player_2
    global player_3
    # bot.send_message(message.chat.id, 'Отлично!')
    if message.chat.id == support.ID or message.chat.id == master.ID:
        if message.text == 'Счет':
            bot.send_message(message.chat.id, player_1.name + ': ' + player_1.score.__str__() + ' или ' + (
                        player_1.score / 100).__str__() + ' конф')
            bot.send_message(message.chat.id, player_2.name + ': ' + player_2.score.__str__() + ' или ' + (
                        player_2.score / 100).__str__() + ' конф')
            bot.send_message(message.chat.id, player_3.name + ': ' + player_3.score.__str__() + ' или ' + (
                        player_3.score / 100).__str__() + ' конф')
        if message.text == 'Новый вопрос':
            if counter > 1:
                counter = 0
                print("==============================================")
    if message.chat.id == support.ID:
        if message.text == '200' or message.text == '400' or message.text == '600' or message.text == '800':
            keyboard = telebot.types.ReplyKeyboardMarkup(True)
            button_1 = telebot.types.KeyboardButton(player_1.name)
            keyboard.add(button_1)
            button_2 = telebot.types.KeyboardButton(player_2.name)
            keyboard.add(button_2)
            button_3 = telebot.types.KeyboardButton(player_3.name)
            keyboard.add(button_3)
            button_4 = telebot.types.KeyboardButton('Отмена')
            keyboard.add(button_4)
            bot.send_message(message.chat.id, 'Выберите игрока!', reply_markup=keyboard)
            support.score = int(message.text)
        elif message.text == 'Отмена':
            buildSupportButtons(message)
        if message.text == player_1.name:
            player_1.score += support.score
            bot.send_message(player_1.ID, 'Правильный ответ! Вот твои ' + (support.score / 100).__str__() + ' конф')
            buildSupportButtons(message)
        elif message.text == player_2.name:
            player_2.score += support.score
            bot.send_message(player_2.ID, 'Правильный ответ! Вот твои ' + (support.score / 100).__str__() + ' конф')
            buildSupportButtons(message)
        elif message.text == player_3.name:
            player_3.score += support.score
            bot.send_message(player_3.ID, 'Правильный ответ! Вот твои ' + (support.score / 100).__str__() + ' конф')
            buildSupportButtons(message)
    else:
        # Игра пользователя
        if message.text == 'Ответ готов!':
            dt = datetime.datetime.now().__str__()
            counter += 1
            text = counter.__str__() + ' ' + dt + ' ' + message.chat.first_name
            if counter == 1:
                bot.send_message(message.chat.id, "(№1) Отлично. Твой ответ?")
                bot.send_message(master.ID, "Отвечает: " + message.chat.first_name)
                bot.send_message(support.ID, "Отвечает: " + message.chat.first_name)
            elif counter == 2:
                bot.send_message(message.chat.id, "(№2) Эх, почти ...")
            elif counter == 3:
                bot.send_message(message.chat.id, "(№3) Почётное 3 место!")
            else:
                bot.send_message(message.chat.id, "(№4+) ( ??? )")
            print(text)
        # Создание пользователя
        elif message.text == 'Пустой слот 1':
            if player_1.ready:
                bot.send_message(message.chat.id, "Выбери другой слот. Этот уже занят!")
            else:
                player_1.name = message.chat.first_name
                player_1.ID = message.chat.id
                player_1.ready = True
                buildButtons(message)
        elif message.text == 'Пустой слот 2':
            if player_2.ready:
                bot.send_message(message.chat.id, "Выбери другой слот. Этот уже занят!")
            else:
                player_2.name = message.chat.first_name
                player_2.ID = message.chat.id
                player_2.ready = True
                buildButtons(message)
        elif message.text == 'Пустой слот 3':
            if player_3.ready:
                bot.send_message(message.chat.id, "Выбери другой слот. Этот уже занят!")
            else:
                player_3.name = message.chat.first_name
                player_3.ID = message.chat.id
                player_3.ready = True
                buildButtons(message)


def clear_counter():
    global counter
    threading.Timer(3.0, clear_counter).start()
    if counter > 1:
        counter = 0
        print("==============================================")


clear_counter()

bot.polling(none_stop=True, interval=0)
