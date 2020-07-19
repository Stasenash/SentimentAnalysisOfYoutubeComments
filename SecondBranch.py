import YouTubeParser
import DB
import Comments_downloader
import Essences
import Additionally
from data_analyzer import DataAnalyzer

import os
import io
import json
import pymorphy2
from tqdm import tqdm
import matplotlib.pyplot as plt
#%%
class SecondBranch_actions:
    
    def __init__(self, channel_link):
        
        self.channel_link = channel_link
        self.symbols = ['"', "'", '(', ')', ':', '\n', '~', '`', '»', '«', '@']
        self.youtube = YouTubeParser.YouTubeAPI()
        self.stopwords = ['это', 'еще', 'ещё', 'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между']
        self.morph = pymorphy2.MorphAnalyzer()
        self.subs = Additionally.GetDescryption()
        self.sentiment = {'EngModel': 87.628866, 'RusModel': 76.14678899, 'DostModel': 56.40243902}
        self.analysis_string = ''
        
        try:
            video_database = DB.Video_DB('VideoDatabase')
            self.communication = DB.Interaction(video_database)
            self.communication.create_table('Videoclips')
            self.communication.create_table_for_comments()
        except:
            pass
        
        
    def data_full_check(self, dictionary):
        
        try:
            video_id = dictionary['id']
        except:
            video_id = 'Значение не определено'
        try:
            channel_name = dictionary['snippet']['channelTitle']           
        except:
            channel_name = 'Значение не определено'           
        try:
            video_name = dictionary['snippet']['title']
        except:
            video_name = 'Значение не определено'
        try:
            commentCount = dictionary['statistics']['commentCount']
        except:
            commentCount = '0'
        try:
            likesCount = dictionary['statistics']['likeCount']
        except:
            likesCount = '0'
        try:
            dislikesCount = dictionary['statistics']['dislikeCount']
        except:
            dislikesCount = '0'
        try:
            relation = str(f"""лайков - {round(int(dictionary['statistics']['likeCount'])/(int(dictionary['statistics']['likeCount'])+int(dictionary['statistics']['dislikeCount']))*100)}%, дизлайков - {round(int(dictionary['statistics']['dislikeCount'])/(int(dictionary['statistics']['likeCount'])+int(dictionary['statistics']['dislikeCount']))*100)}%""")
        except:
            relation = 'Значение не определено'
        try:
            viewsCount = dictionary['statistics']['viewCount']
        except:
            viewsCount = '0'
        try:
            tagsCount = len(dictionary['snippet']['tags'])
        except:
            tagsCount = '0'
        try:
            video_duration = dictionary['contentDetails']['duration']
        except:
            video_duration = 'Значение не определено'
        try:
            video_description = dictionary['snippet']['description']
        except:
            video_description = 'Значение не определено'
        
        return [video_id, channel_name, video_name, commentCount, likesCount, dislikesCount, relation, viewsCount, tagsCount, video_duration, video_description]
   
    
    def write_to_the_database(self):
        
        items = self.data_full_check(self.youtube.all_info)
        
        video_object = Essences.Video(items[0], items[1],
                                   items[2], self.youtube.language, 
                                   items[3], items[4], items[5],
                                   items[6], items[7], items[8], items[9], 
                                   items[10], self.analysis_string)
    
        self.communication.input_data(video_object)
#        
        
    def create_folders(self):
        channel_dir = f"Analysis/{self.youtube.channel['id']}_{self.youtube.channel['snippet']['title']}"

        if not os.path.exists(channel_dir):
            os.mkdir(channel_dir)
        else:
            pass
            
        return channel_dir
    
    
    def lead_to_initial_form(self, variable):
        
        words = variable.lower().split()
        string = ""
        norm_tokens = []
        
        for i in tqdm(words):
            nf = self.morph.parse(i)[0].normal_form
            norm_tokens.append(nf)
            
        norm_tokens = [i for i in norm_tokens if i not in self.stopwords]
        
        for i in norm_tokens:
            string += i + " "
            
        return string
    
    
    def get_ids_from_video(self):
        
        try:
            all_info = self.youtube.download_channel_videos(self.channel_link)
            list_ids = []
    
            for playlist in all_info:
                for dict_info in playlist:
                    list_ids.append(dict_info['contentDetails']['videoId'])
            
            return list_ids
        except:
            print('The channel does not have playlists')
    
    
    def make_WorldCloud_picture(self): 
        
        list_ids = self.get_ids_from_video()
        clear_text = ''
        
        for _id in list_ids:
            exist = self.communication.print_comments(_id)
                
            if exist == False:
                pass
            
            else:
                for comment in exist:
                    comment_text = comment[1]
                    clear_text += self.lead_to_initial_form(comment_text)
                    
        self.subs.get_WordCloud(clear_text)

    
    def get_channel_info(self):
        
        info = self.youtube.get_channel_from_url(self.channel_link)
        
        if info['snippet']['description'] == '':
            info['snippet']['description'] = 'Описание отсутствует'
        else:
            pass
        
        information = f"""
        Название канала: {info['snippet']['title']}
        Дата основания канала: {info['snippet']['publishedAt']}
        Общее число просмотров: {info['statistics']['viewCount']}
        Количество подписчиков: {info['statistics']['subscriberCount']}
        Общее количество видеороликов на канале: {info['statistics']['videoCount']}
        Авторское описание канала: 
            
{info['snippet']['description']}
        """

        return information
    
    
    def get_comments_text(self, video_id):
        
        self.channel_dir = self.create_folders()
        file_name = f'{self.channel_dir}/{video_id}.json'
        comments = []
        self.text = ''

        if os.path.exists(file_name):
            pass
        
        args = ['-y', f" {video_id}", '-o', file_name, '-l', '10000']
        
        Comments_downloader.main(args)
         
        with io.open(file_name, 'r', encoding='utf8') as fj:
            data = fj.readlines()
        
            for line in data:  
                dictionary = json.loads(line)
                comments.append(dictionary['text'])
                
            for comment in tqdm(comments):
                for n in self.symbols:                    
                    clear_comment = comment.replace(n, '')
                
                try:
                    self.communication.insert_into_comments_table(video_id, clear_comment)
                    
                except:
                    pass
     
    
    def sentiment_eng_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:

            analysis_dictionary = DataAnalyzer.get_eng_analysis(massive_comments)
            self.analysis_string += f"Анализ первой(положительные) - {analysis_dictionary['positive']}, анализ первой(негативные) - {analysis_dictionary['negative']}"
            
        
        
    def sentiment_rus_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:

            analysis_dictionary = DataAnalyzer.get_rus_analysis(massive_comments)
            self.analysis_string += f"Анализ второй(положительные) - {analysis_dictionary['positive']}, анализ второй(негативные) - {analysis_dictionary['negative']}"
            
        
        
    def sentiment_dost_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:
            analysis_dictionary = DataAnalyzer.get_rus_analysis(massive_comments)
            self.analysis_string += f"Анализ третьей(положительные) - {analysis_dictionary['positive']}, анализ третьей(негативные) - {analysis_dictionary['negative']}"
                    
    

    def alysis_histogram(self, massive_pos_1, massive_neg_1, massive_pos_2, massive_neg_2, massive_pos_3, massive_neg_3):
        
        x1 = ['positive_1', 'negative_1']
        x2 = ['positive_2', 'negative_2']
        x3 = ['positive_3', 'negative_3']
        y1 = [sum(massive_pos_1)/(len(massive_pos_1)), sum(massive_neg_1)/len(massive_neg_1)]
        y2 = [sum(massive_pos_2)/len(massive_pos_2), sum(massive_neg_2)/len(massive_neg_2)]
        y3 = [sum(massive_pos_3)/len(massive_pos_3), sum(massive_neg_3)/len(massive_neg_3)]
    
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        ax.bar(x3, y3, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью алгоритмов нейронных сетей')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_1')
        
        
    def get_info_from_video(self):
        
        self.likes = []
        self.dislikes = []
        self.commentsCount = []
        self.views = []
        massive_comments = []
        self.massive_pos_1 = []
        self.massive_neg_1 = []
        self.massive_pos_2 = []
        self.massive_neg_2 = []
        self.massive_pos_3 = []
        self.massive_neg_3 = []
        
        ids = self.get_ids_from_video()
        
        for _id in ids:
            actuality = self.communication.check_actuality_by_id(_id) 
                  
            if actuality == False:
                
                try:
                    self.youtube.get_video_info(_id)
                    self.get_comments_text(_id)
                    
                    massive_data = self.communication.print_comments(_id)
                
                    for comments in massive_data:
                        massive_comments.append(comments[1])
                        
                    self.sentiment_eng_analysis(massive_comments) 
                    self.sentiment_rus_analysis(massive_comments)
                    self.sentiment_dost_analysis(massive_comments)              
                    
                    self.write_to_the_database()
                    self.analysis_string = ''
                    
                except:
                    pass
                
            else:
                pass
            
            video = self.communication.extract_obj_by_id(_id)

            self.likes.append(int(video[0][5]))
            self.dislikes.append(int(video[0][6]))
            self.commentsCount.append(int(video[0][4]))
            self.views.append(int(video[0][8]))
            
            analysis = video[0][-2]
            string = analysis.split('-')
            
            self.massive_pos_1.append(float(string[1][1:6]))
            self.massive_neg_1.append(float(string[2][1:6]))
            self.massive_pos_2.append(float(string[3][1:6]))
            self.massive_neg_2.append(float(string[4][1:6]))
            self.massive_pos_3.append(float(string[5][1:6]))
            self.massive_neg_3.append(float(string[6][1:6]))
            
        
    def analysis_of_comments_for_a_single_channel(self):
        
        print(self.get_channel_info())
        
        self.get_info_from_video()   
        print(f"Максимальное количество комментариев: {max(self.commentsCount)}")
        print(f"Минимальное количество комментариев: {min(self.commentsCount)}")
        print(f"Максимальное количество лайков: {max(self.likes)}")
        print(f"Минимальное количество лайков: {min(self.likes)}")
        print(f"Максимальное количество дизлайков: {max(self.dislikes)}")
        print(f"Минимальное количество дизлайков: {min(self.dislikes)}")
        print(f"Максимальное количество просмотров: {max(self.views)}")
        print(f"Минимальное количество просмотров: {min(self.views)}")
        self.alysis_histogram(self.massive_pos_1,
                              self.massive_neg_1,
                              self.massive_pos_2,
                              self.massive_neg_2,
                              self.massive_pos_3,
                              self.massive_neg_3)
        string = f"""Точность первой нейронной сети: {self.sentiment['EngModel']}
                     Точность второй нейронной сети: {self.sentiment['RusModel']}
                     Точность третьей нейронной сети: {self.sentiment['DostModel']}"""   
        print(string)
        
        
# #%%
# second = SecondBranch_actions('https://www.youtube.com/user/InokTV')
# ##%%
# second.analysis_of_comments_for_a_single_channel()
# #
# ##%%
# second.make_WorldCloud_picture()
# #%%'
