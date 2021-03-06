import telebot

import DB
import keyboards
import states
from analysis_of_one_video import AnalysisOfOneVideoActions
from analysis_of_two_videos import AnalysisOfTwoVideosActions
from analysis_of_one_channel import AnalysisOfOneChannelActions
import datetime as dt
from blogers_wordcloud import BlogersWordcloudActions

DataBase = DB.Video_DB('VideoDatabase')
interaction = DB.Interaction(DataBase)
interaction.create_user_table()
interaction.create_statistic_table()
interaction.create_table_for_admins()
interaction.create_favourites_table()


def GetState(message):
    if message.from_user.username is not None:
        data = interaction.get_user_state(str(message.from_user.username))
        state = int(data[0][1])
    else:
        data = interaction.get_user_state(str(message.from_user.id))
        state = int(data[0][1])
    return state


def SetState(message, number_state):
    if message.from_user.username is not None:
        interaction.update_state_in_user_table(str(message.from_user.username), str(number_state))
    else:
        interaction.update_state_in_user_table(str(message.from_user.id), str(number_state))


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
        SetState(message, 71)


    elif message.text == "Удалить администратора":
        bot.send_message(message.chat.id,
                         "Введите username пользователя, которого вы хотите убрать из списка администраторов")
        SetState(message, 72)

    elif message.text == "Посмотреть статистику":  # новые + за неделю
        bot.send_message(message.chat.id, "Статистика", reply_markup=keyboards.statistics_keyboard())

    elif message.text == "Новые пользователи":  # за день за неделю
        bot.send_message(message.chat.id, "Новые пользователи", reply_markup=keyboards.newusers_keyboard())

    elif message.text == "За день":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        today_date = dt.date.today()
        data = interaction.check_new_users(today_date)
        if data == []:
            bot.send_message(message.chat.id, f'Количество новых пользователей за день: 0', reply_markup=keyboards.back_keyboard())
        else:
            bot.send_message(message.chat.id, f'Количество новых пользователей за день: {len(data)}', reply_markup=keyboards.back_keyboard())


    elif message.text == "За неделю":
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        today_date = dt.date.today()
        quantity = interaction.check_week_new_users()
        if quantity == []:
            bot.send_message(message.chat.id, f'Количество новых пользователей за неделю: 0', reply_markup=keyboards.back_keyboard())
        else:
            bot.send_message(message.chat.id, f'Количество новых пользователей за неделю: {quantity[0][0]}', reply_markup=keyboards.back_keyboard())

    elif message.text == "Действия пользователей за неделю":  # юзернейм действие по датам (неделя)
        bot.send_message(message.chat.id, "Выводим статистику", reply_markup=keyboards.back_keyboard())
        string = ''
        action_ac = interaction.print_actions_from_statistic_table('ac')
        if action_ac == []:
            string += 'Анализ комментариев под видео: 0 раз\n'
        else:
            string += f'Анализ комментариев под видео: {len(action_ac)} раз' + '\n'

        action_cc = interaction.print_actions_from_statistic_table('cc')
        if action_cc == []:
            string += 'Сравнение двух видео: 0 раз\n'
        else:
            string += f'Сравнение двух видео: {len(action_cc)} раз' + '\n'

        action_ach = interaction.print_actions_from_statistic_table('ach')
        if action_ach == []:
            string += 'Анализ комментариев на канале: 0 раз\n'
        else:
            string += f'Анализ комментариев на канале: {len(action_ach)} раз' + '\n'

        action_wcb = interaction.print_actions_from_statistic_table('wcb')
        if action_wcb == []:
            string += 'Wordcloud речи блогера: 0 раз\n'
        else:
            string += f'Wordcloud речи блогера: {len(action_wcb)} раз' +'\n'

        bot.send_message(message.chat.id, string, reply_markup=keyboards.back_keyboard())


    elif message.text == "Анализ комментариев":
        bot.send_message(message.chat.id, "Проанализировать комментарии...", reply_markup=keyboards.analysis_keyboard())

    elif message.text == "Сравнение комментариев":
        bot.send_message(message.chat.id, "Сравнить комменарии...", reply_markup=keyboards.compare_keyboard())

    elif message.text == "Wordcloud анализ речи блогера":
        bot.send_message(message.chat.id, "Введите ссылку на видео", reply_markup=keyboards.back_keyboard())
        SetState(message, 6)


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
        SetState(message, 1)


    elif message.text == "На канале":
        bot.send_message(message.chat.id, "Введите ссылку на канал", reply_markup=keyboards.back_keyboard())
        SetState(message, 2)

    elif message.text == "Под двумя видео":
        bot.send_message(message.chat.id, "Введите ссылку на первое видео", reply_markup=keyboards.back_keyboard())
        SetState(message, 31)

    elif message.text == "На двух каналах":
        bot.send_message(message.chat.id, "Введите ссылку на первый канал", reply_markup=keyboards.back_keyboard())
        SetState(message, 41)

    elif message.text == "Посмотреть избранное":
        bot.send_message(message.chat.id, "Выводим список избранных", reply_markup=keyboards.back_keyboard())
        if message.from_user.username is not None:
            favourites = interaction.print_favorites_table(message.from_user.username)
        else:
            favourites = interaction.insert_into_statistic_table(str(message.from_user.id))
        count = 1
        string = ''
        for i in favourites:
            string += f'{count}. i[1]'

        bot.send_message(message.chat.id, string, reply_markup=keyboards.back_keyboard())

    elif message.text == "Добавить в избранное":
        # проверка на количесвто избранных (макс 10)
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите добавить в избранное", reply_markup=keyboards.back_keyboard())
        SetState(message, 51)

    elif message.text == "Удалить из избранного":
        bot.send_message(message.chat.id, "Введите ссылку, которую вы хотите удалить из избранного",
                         reply_markup=keyboards.back_keyboard())
        SetState(message, 52)

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
        if GetState(message) == 1:
            try:
                if message.from_user.username is not None:
                    interaction.insert_into_statistic_table(message.from_user.username, "ac")
                else:
                    interaction.insert_into_statistic_table(str(message.from_user.id), "ac")

                bot.link_video1 = message.text
                analysis_a_single_video = AnalysisOfOneVideoActions(bot.link_video1)
                bot.send_message(message.chat.id,
                                 "Анализ комментариев может занять некоторое время, пожалуйста, дождитесь результата.")
                video_info, string = analysis_a_single_video.analysis_of_comments_for_a_single_video()
                bot.send_message(message.chat.id, video_info)
                bot.send_message(message.chat.id, string)

                for i in range(1, 4):
                    photo = open(f'Figures/fig_video_{analysis_a_single_video.id_video}_{i}.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
            except:
                bot.send_message(message.chat.id, "Произошла непредвиденная ошибка, попробуйте еще раз. Если ошибка "
                                                  "не исправляется - попробуйте удалить чат с ботом и попробовать "
                                                  "сначала")
            SetState(message, 0)
        elif GetState(message) == 6:
            try:
                if message.from_user.username is not None:
                    interaction.insert_into_statistic_table(message.from_user.username, "wcb")
                else:
                    interaction.insert_into_statistic_table(str(message.from_user.id), "wcb")
                link_video6 = message.text
                bot.send_message(message.chat.id, "Выводим wordcloud анализ", reply_markup=keyboards.back_keyboard())
                analysis_a_bloger_speech = BlogersWordcloudActions(link_video6)
                analysis_a_bloger_speech.get_wordcloud_picture()
                wphoto = open('Figures/picture_new.png', 'rb')
                bot.send_photo(message.chat.id, wphoto)
            except:
                pass
            SetState(message, 0)

        elif GetState(message) == 31:
            bot.link_video31 = message.text
            SetState(message, 32)
            bot.send_message(message.chat.id, "Введите ссылку на второе видео", reply_markup=keyboards.back_keyboard())

        elif GetState(message) == 32:
            try:
                if message.from_user.username is not None:
                    interaction.insert_into_statistic_table(message.from_user.username, "cc")
                else:
                    interaction.insert_into_statistic_table(str(message.from_user.id), "cc")
                link_video32 = message.text
                bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
                compare_the_two_videos = AnalysisOfTwoVideosActions(bot.link_video31, link_video32)
                compare_the_two_videos.comparative_analysis()
                for i in range(1, 7):
                    photo = open(f'Figures/fig_video_comparison_{i}.png', 'rb')
                    bot.send_photo(message.chat.id, photo)
                SetState(message, 0)
            except:
                bot.send_message(message.chat.id, "Произошла непредвиденная ошибка, попробуйте еще раз. Если ошибка "
                                                  "не исправляется - попробуйте удалить чат с ботом и попробовать "
                                                  "сначала")

        else:
            link_video6 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
            # картинка
            # занесение в бд действия пользователя
            SetState(message, 0)

    elif message.text[0:28] == "https://www.youtube.com/user" or message.text[
                                                                 0:31] == "https://www.youtube.com/channel":
        if GetState(message) == 2:
            try:
                if message.from_user.username is not None:
                    interaction.insert_into_statistic_table(message.from_user.username, "ach")
                else:
                    interaction.insert_into_statistic_table(str(message.from_user.id), "ach")

                link_channel2 = message.text
                bot.send_message(message.chat.id, "Выводим анализ")  # , reply_markup=keyboards.wordcloud_keyboard()
                analysis_one_channel = AnalysisOfOneChannelActions(link_channel2)
                string = analysis_one_channel.analysis_of_comments_for_a_single_channel()
                bot.send_message(message.chat.id, string)
                photo = open(f'Figures/fig_channel_1.png', 'rb')
                bot.send_photo(message.chat.id, photo)
                SetState(message, 0)
            except:
                bot.send_message(message.chat.id, "Произошла непредвиденная ошибка, попробуйте еще раз. Если ошибка "
                                                  "не исправляется - попробуйте удалить чат с ботом и попробовать "
                                                  "сначала")

        elif GetState(message) == 41:
            link_channel41 = message.text
            bot.send_message(message.chat.id, "Введите ссылку на второй канал", reply_markup=keyboards.back_keyboard())
            SetState(message, 42)

        else:
            link_channel42 = message.text
            bot.send_message(message.chat.id, "Выводим анализ", reply_markup=keyboards.back_keyboard())
            # занесение в бд дей-ия пользователя
            # вывод анализа + картинок
            SetState(message, 0)

    elif message.text[0:23] == "https://www.youtube.com":
        if GetState(message) == 51:  # getstate
            link_fav51 = message.text
            data = interaction.check_in_favourites(link_fav51)
            if data == []:
                bot.send_message(message.chat.id, "Данная ссылка уже существует в Избранном", reply_markup=keyboards.back_keyboard())
            else:
                if message.from_user.username is not None:
                    interaction.insert_into_favourites_table(message.from_user.username,link_fav51)
                else:
                    interaction.insert_into_favourites_table(str(message.from_user.id), link_fav51)
            SetState(message, 0)

        elif states.GetState(message) == 52:
            link_fav52 = message.text
            # удалить из избранного
            bot.send_message(message.chat.id, "Ссылка удалена из избранного",
                             reply_markup=keyboards.back_keyboard())
            SetState(message, 0)

        else:
            bot.send_message(message.chat.id, "Возникла ошибка.")
            SetState(message, 0)

    else:
        if GetState(message) == 71:
            try:
                username71 = message.text #TODO ошибка с админкой
                if interaction.get_user_admin(username71) is None \
                        and interaction.get_user(username71) is not None:
                    interaction.insert_into_admins_table(username71)
                    bot.send_message(message.chat.id, "Новый администратор добавлен",
                                     reply_markup=keyboards.back_keyboard())
                else:
                    bot.send_message(message.chat.id, "Добавление не удалось. Возможно, такого пользователя не "
                                                      "существует, или он уже является администратором",
                                     reply_markup=keyboards.back_keyboard())
            except:
                pass
            SetState(message, 0)

        elif GetState(message) == 72:
            try:
                username72 = message.text
                interaction.delete_from_admins_table(username72)
                bot.send_message(message.chat.id, "Администратор удален", reply_markup=keyboards.back_keyboard())
            except:
                pass
            SetState(message, 0)

        else:
            bot.send_message(message.chat.id, "Возникла ошибка. Была введена неизвестная команда или неверная ссылка"
                                              "\nНапишите /help")
            SetState(message, 0)


bot.polling(none_stop=True, interval=0)
