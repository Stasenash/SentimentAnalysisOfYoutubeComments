#import Comments_downloader
#import YouTubeParser
#from tqdm import tqdm
#import os
#import json
#import io
#import datetime as dt
#
#import Essences
#import DB
#
#database = DB.Video_DB('film_database')
#action = DB.Interaction(database)
#action.create_table('Films')
#print('Таблица создана')
##%%
#link = 'https://www.youtube.com/watch?v=aTUJoiJOFV4'
#youtube = YouTubeParser.YouTubeAPI(link)
#youtube.get_video_info()
#
##%%
#channel_dir = f"Analysis/{youtube.all_info['snippet']['channelId']}_{youtube.all_info['snippet']['channelTitle']}"
#
#if not os.path.exists(channel_dir):
#    os.mkdir(channel_dir)
#else:
#    print(f'Каталог {channel_dir} уже существует')
#
#symbols = ['"', "'", '(', ')', ':', '\n', '~', '`', '»', '«']
#    
##%%
#for i in tqdm(range(len(youtube.video_ids))):
#    
#    video_id = youtube.video_ids[i] 
#    file_name = f'{channel_dir}/{video_id}.json'
#    text = ''
#    print(text)
#    
#    
#    if os.path.exists(file_name):
#        print(f'Файл {file_name} существует')
#        continue
#    
#    args = ['-y', f" {video_id}", '-o', file_name, '-l', '10000']
#    
#    Comments_downloader.main(args)
# 
#    print('Комментарии скачены')
#    
#    with io.open(file_name, 'r', encoding='utf8') as fj:
#        data = fj.readlines()
#        
#        for line in data:            
#            dictionary =  json.loads(line)
#            text += dictionary['text']
#            
#        for i in symbols: 
#            text = text.replace(i, '')
#                
#
#    print(type(text))
#
#
#    film_object = Essences.Film(link, youtube.all_info['snippet']['channelTitle'],
#                               youtube.all_info['snippet']['title'], youtube.language, 
#                               youtube.all_info['statistics']['commentCount'], youtube.all_info['statistics']['likeCount'],
#                               youtube.all_info['statistics']['dislikeCount'], str(f"""лайков - {round(int(youtube.all_info['statistics']['likeCount'])/(int(youtube.all_info['statistics']['likeCount'])+int(youtube.all_info['statistics']['dislikeCount']))*100)}%,
#                                                                                       дизлайков - {round(int(youtube.all_info['statistics']['dislikeCount'])/(int(youtube.all_info['statistics']['likeCount'])+int(youtube.all_info['statistics']['dislikeCount']))*100)}%"""),                                                              
#                               youtube.all_info['statistics']['viewCount'],
#                               len(youtube.all_info['snippet']['tags']), youtube.all_info['contentDetails']['duration'],
#                               youtube.all_info['snippet']['description'], text)
#    
#    print('Создан объект')
#
#
##%%
#    
#    video = action.extract_obj(link)
#    video_link = video[0][0]
#    
#    print(video_link)
#
#    
#
#    
#    
#
#    
##%%
#a = [('a', 'b', 'c')]
#
#print(a[0][0])