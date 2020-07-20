from telebot import types

user_role="admin"

def main_keyboard(message):
    keyboardmain = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    if message.from_user.username == "Stasenash": #проверка что текущий юзернейм есть в табл админов
        keyboardmain.add("Функции администратора")

    keyboardmain.add("Анализ комментариев")
    keyboardmain.add("Сравнение комментариев")
    keyboardmain.add("Wordcloud анализ речи блогера")
    keyboardmain.row("Избранное", "История")

    return keyboardmain

def admin_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Добавить нового администратора")
    keyboard.add("Удалить администратора")
    keyboard.add("Посмотреть статистику")
    keyboard.add("Назад")

    return keyboard

def statistics_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Новые пользователи")
    keyboard.add("Действия пользователей за неделю")
    keyboard.add("Назад")

    return keyboard

def newusers_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("За день")
    keyboard.add("За неделю")
    keyboard.add("Назад")

    return keyboard

def analysis_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Под видео")
    keyboard.add("На канале")
    keyboard.add("Назад")

    return keyboard


def compare_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Под двумя видео")
    keyboard.add("На двух каналах")
    keyboard.add("Назад")

    return keyboard

def back_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Назад")

    return keyboard

def fav_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Посмотреть избранное")
    keyboard.add("Добавить в избранное")
    keyboard.add("Удалить из избранного")
    keyboard.add("Назад")

    return keyboard

def wordcloud_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    keyboard.add("Wordcloud")
    keyboard.add("Назад")

    return keyboard
