import DB

DataBase = DB.Video_DB('VideoDatabase')
interaction = DB.Interaction(DataBase)

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


# 0 - состояние "спокойствия". Пользователь не отдает нам никаких ссылок
# 1 - пользователь отдает ссылку для анализа комментариев под видео
# 2 - пользователь отдает ссылку для анализа комментариев на канале
# 31 - пользователь отдает первую ссылку для сравнения видео
# 32 - пользователь отдает вторую ссылку для сравнения видео
# 41 - пользователь отдает первую ссылку для сравнения каналов
# 42 - пользователь отдает вторую ссылку для сравнения каналов
# 51 - пользователь отдает ссылку для добавления в избранное
# 52 - пользователь отдает ссылку для удаления из избранного
# 6 - пользователь отдает ссылку для wordcloud анализа речи блогера
# 71 - админ отдает username пользователя, которого хочет сделать администратором
# 72 - админ отдает username пользователя, которого хочет лишить прав администратора