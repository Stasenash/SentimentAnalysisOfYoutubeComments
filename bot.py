import telebot
import keyboards
import states

import DB

DataBase = DB.Video_DB('VideoDatabase')
interaction = DB.Interaction(DataBase)
interaction.create_user_table()

bot = telebot.TeleBot('1253043081:AAE_gKsMqeHl-4lBY9hRqWqbHfi_AuPsj-M')

link_video1 = ""
link_video31 = ""
link_video32 = ""
link_video6 = ""

link_channel2 = ""
link_channel41 = ""
link_channel42 = ""

link_fav51 = ""
link_fav52 = ""

username71 = ""
username72 = ""

state = 0


@bot.message_handler(commands=['start'])
def start_work(message):
    # Вот здесь происходит запись username (message.from_user.username) пользователя, если его нет, то записывает айдишник(message.from_user.id)
    try:
        if message.from_user.username is not None:
            interaction.insert_into_user_table(message.from_user.username, 0)
        else:
            interaction.insert_into_user_table(str(message.from_user.id), 0)
    except:
        pass
    bot.send_message(message.chat.id,
                     "Обращаем ваше внимание на то, что ссылки, который вы подаете боту, должны быть в следующем формате:"
                     "\nВидео: https://www.youtube.com/watch?v***"
                     "\nКанал: https://www.youtube.com/channel/***  или \nhttps://www.youtube.com/user/***",
                     reply_markup=keyboards.main_keyboard(message))


@bot.message_handler(content_types=['text'])
def processing_message(message):
    if message.text == "Функции администратора":
        bot.send_message(message.chat.id, "Функции администратора", reply_markup=keyboards.admin_keyboard())

    elif message.text == "Добавить нового администратора":
        bot.send_message(message.chat.id, "Введите username пользователя, которого вы хотите сделать администратором")
        states.SetState(message, 71)


    elif message.text == "Удалить администратора":
        bot.send_message(message.chat.id,
                         "Введите username пользователя, которого вы хотите убрать из списка администраторов")
        states.SetState(message, 72)

    elif message.text == "Посмотреть статистику":  # новые + за неделю
        bot.send_message(message.chat.id, "Статистика", reply_markup=keyboards.statistics_keyboard())

    elif message.text == "Новые пользователи":  # за день за неделю
        bot.send_message(message.chat.id, "Новые пользователи", reply_markup=keyboards.newusers_keyboard())

    elif message.text == "За день":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())

    elif message.text == "За неделю":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())

    elif message.text == "Действия пользователей за неделю":  # юзернейм действие по датам (неделя)
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())

    elif message.text == "Анализ комментариев":
        bot.send_message(message.chat.id, "Проанализировать комментарии...", reply_markup=keyboards.analysis_keyboard())

    elif message.text == "Сравнение комментариев":
        bot.send_message(message.chat.id, "Сравнить комменарии...", reply_markup=keyboards.compare_keyboard())

    elif message.text == "Wordcloud анализ речи блогера":
        bot.send_message(message.chat.id, "Введите ссылку на видео", reply_markup=keyboards.back_keyboard())
        states.SetState(message, 6)


    elif message.text == "Избранное":
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboards.fav_keyboard())

    elif message.text == "История":
        # выводим список из 10 последний ссылок
        bot.send_message(message.chat.id, "История", reply_markup=keyboards.back_keyboard())
        bot.send_message(message.chat.id, "Список 10 последних ссылок")

    elif message.text == "Назад":
        bot.send_message(message.chat.id, "Что вы хотите сделать?", reply_markup=keyboards.main_keyboard(message))

    elif message.text == "Под видео":
        bot.send_message(message.chat.id, "Введите ссылку на видео", reply_markup=keyboards.back_keyboard())
        states.SetState(message, 1)


    elif message.text == "На канале":
        bot.send_message(message.chat.id, "Введите ссылку на канал", reply_markup=keyboards.back_keyboard())
        states.SetState(message, 2)

    elif message.text == "Под двумя видео":
        bot.send_message(message.chat.id, "Введите ссылку на первое видео", reply_markup=keyboards.back_keyboard())
        states.SetState(message, 31)

    elif message.text == "На двух каналах":
        bot.send_message(message.chat.id, "Введите ссылку на первый канал", reply_markup=keyboards.back_keyboard())
        states.SetState(message, 41)

    elif message.text == "Посмотреть избранное":
        bot.send_message(message.chat.id, "Выводим список избранных", reply_markup=keyboards.back_keyboard())

    elif message.text == "Добавить в избранное":
        # проверка на количесвто избранных (макс 10)
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите добавить в избранное",
                         reply_markup=keyboards.back_keyboard())
        states.SetState(message, 51)

    elif message.text == "Удалить из избранного":
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите удалить из избранного",
                         reply_markup=keyboards.back_keyboard())
        states.SetState(message, 52)

    elif message.text == "Wordcloud":
        bot.send_message(message.chat.id, "Выводим wordcloud анализ", reply_markup=keyboards.back_keyboard())
        # занесение в бд
        # картинка

    elif message.text == "Привет" or message.text == "привет":
        bot.send_message(message.chat.id, "Доброго времени суток! Что вы хотите сделать?",
                         reply_markup=keyboards.main_keyboard(message))

    elif message.text == "/help":
        bot.send_message(message.chat.id,
                         "Если возникла ошибка после ввода ссылки => была введена неверная ссылка. Попробуйте ввести другую "
                         "\nЕсли вы не знаете как начать со мной работать => просто напишите мне 'Привет'"
                         "\nОбращаем ваше внимание на то, что ссылки, который вы подаете боту, должны быть в следующем формате:"
                         "\nВидео: https://www.youtube.com/watch?v***"
                         "\nКанал: https://www.youtube.com/channel/***  или \nhttps://www.youtube.com/user/***")




    elif message.text[0:31] == "https://www.youtube.com/watch?v":
        if states.GetState(message) == 1:
            link_video1 = message.text
            bot.send_message(message.chat.id, "dkflvnjhdkjvn", reply_markup=keyboards.back_keyboard())
            # отдать статистику
            # занесение в бд дей - ия пользователя
            # вывод анализа + картинок
            states.SetState(message, 0)

        elif states.GetState(message) == 31:
            link_video31 = message.text
            states.SetState(message, 32)
            bot.send_message(message.chat.id, "Введите ссылку на второе видео", reply_markup=keyboards.back_keyboard())

        elif states.GetState(message) == 32:
            link_video32 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
            # отдать статистику
            # записываем действия
            states.SetState(message, 0)

        else:
            link_video6 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
            # картинка
            # занесение в бд действия пользователя
            states.SetState(message, 0)

    elif message.text[0:28] == "https://www.youtube.com/user" or message.text[
                                                                 0:31] == "https://www.youtube.com/channel":
        if states.GetState(message) == 2:
            link_channel2 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.wordcloud_keyboard())
            # занесение в бд дей-ия пользователя
            # вывод анализа + картинок
            states.SetState(message, 0)

        elif states.GetState(message) == 41:
            link_channel41 = message.text
            bot.send_message(message.chat.id, "Введите ссылку на второй канал", reply_markup=keyboards.back_keyboard())
            states.SetState(message, 42)

        else:
            link_channel42 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
            # занесение в бд дей-ия пользователя
            # вывод анализа + картинок
            states.SetState(message, 0)

    elif message.text[0:23] == "https://www.youtube.com":
        if states.GetState(message) == 51:  # getstate
            link_fav51 = message.text
            # добавить в избранное
            bot.send_message(message.chat.id, "Ссылка добавлена в избранное",
                             reply_markup=keyboards.back_keyboard())
            states.SetState(message, 0)

        elif states.GetState(message) == 52:
            link_fav52 = message.text
            # удалить из избранного
            bot.send_message(message.chat.id, "Ссылка удалена из избранного",
                             reply_markup=keyboards.back_keyboard())
            states.SetState(message, 0)

        else:
            bot.send_message(message.chat.id, "Возникла ошибка.")
            states.SetState(message, 0)

    else:
        if states.GetState(message) == 71:
            username71 = message.text
            # делаем админом
            bot.send_message(message.chat.id, "Новый администратор добавлен", reply_markup=keyboards.back_keyboard())
            states.SetState(message, 0)

        elif states.GetState(message) == 72:
            username72 = message.text
            # удаляем с админов
            bot.send_message(message.chat.id, "Администратор удален", reply_markup=keyboards.back_keyboard())
            states.SetState(message, 0)

        else:
            bot.send_message(message.chat.id, "Возникла ошибка. Была введена неизвестная команда или неверная ссылка"
                                              "\nНапишите /help")
            states.SetState(message, 0)


bot.polling(none_stop=True, interval=0)