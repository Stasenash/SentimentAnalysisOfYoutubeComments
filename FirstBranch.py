import Comments_downloader
import Additionally
import YouTubeParser
import Essences
import DB
from data_analyzer import DataAnalyzer

from tqdm import tqdm
import os
import json
import io
import pymorphy2
import matplotlib.pyplot as plt

#%%  
class FistBranch_actions():
    
    def __init__(self, link):
        
        self.link = link
        self.symbols = ['"', "'", '(', ')', ':', '\n', '~', '`', '»', '«', '@', '👤', '－', '？']
        self.youtube = YouTubeParser.YouTubeAPI()
        self.stopwords = ['это', 'еще', 'ещё', 'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между']
        self.morph = pymorphy2.MorphAnalyzer()
        self.subs = Additionally.GetDescryption()
        self.id_video = self.youtube.parse_vid_from_url(self.link)
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
        
    
    def create_folders(self):
        channel_dir = f"Analysis/{self.youtube.all_info['snippet']['channelId']}_{self.youtube.all_info['snippet']['channelTitle']}"

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
    
        
    def get_info_about_video(self):
        
        self.youtube.get_video_info(self.id_video)
        
        
    def get_comments_text(self):
        
        comments = []
        self.channel_dir = self.create_folders()
        file_name = f'{self.channel_dir}/{self.id_video}.json'

        if os.path.exists(file_name):
            pass
        
        args = ['-y', f" {self.id_video}", '-o', file_name, '-l', '10000']
        
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
                    self.communication.insert_into_comments_table(self.id_video, clear_comment)
                    
                except:
                    pass

                                          
    def sentiment_eng_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:
            analysis_dictionary = DataAnalyzer.get_eng_analysis(massive_comments)
            self.analysis_string += f"Анализ первой(положительные) - {analysis_dictionary['positive']}, анализ первой(негативные) - {analysis_dictionary['negative']}"
        
    
    def get_histogram_for_analyzing_the_tone_of_comments_first_neural_network(self, value_1, value_2):
        
            x = ['positive', 'negative']
            y = [value_1, value_2]
        
            fig, ax = plt.subplots()
    
            ax.bar(x, y, width = 0.15)
    
            ax.set_facecolor('seashell')
            fig.set_facecolor('floralwhite')
            fig.set_figwidth(6) 
            ax.set_title('Анализ тональности с помощью алгоритма первой нейронной сети')
            fig.set_figheight(6)   
            
            plt.savefig(f'Figures/fig_video_{self.id_video}_1')
            
            
    def sentiment_rus_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:
            analysis_dictionary = DataAnalyzer.get_rus_analysis(massive_comments)
            self.analysis_string += f"Анализ второй(положительные) - {analysis_dictionary['positive']}, анализ второй(негативные) - {analysis_dictionary['negative']}"
        
    
    def get_histogram_for_analyzing_the_tone_of_comments_second_neural_network(self, value_1, value_2):
        
            x = ['positive', 'negative']
            y = [value_1, value_2]
        
            fig, ax = plt.subplots()
    
            ax.bar(x, y, width = 0.15)
    
            ax.set_facecolor('seashell')
            fig.set_facecolor('floralwhite')
            fig.set_figwidth(6) 
            ax.set_title('Анализ тональности с помощью алгоритма второй нейронной сети')
            fig.set_figheight(6)   
            
            plt.savefig(f'Figures/fig_video_{self.id_video}_2')
            
            
    def sentiment_dost_analysis(self, massive_comments):
        
        if massive_comments == False:
            return 'There are no comments on the video, and we cannot analyze it at the moment'
        else:
            analysis_dictionary = DataAnalyzer.get_dost_analysis(massive_comments)
            self.analysis_string += f"Анализ третьей(положительные) - {analysis_dictionary['positive']}, анализ третьей(негативные) - {analysis_dictionary['negative']}"


    def get_histogram_for_analyzing_the_tone_of_comments_third_neural_network(self, value_1, value_2):

            x = ['positive', 'negative']
            y = [value_1, value_2]
        
            fig, ax = plt.subplots()
    
            ax.bar(x, y, width = 0.15)
    
            ax.set_facecolor('seashell')
            fig.set_facecolor('floralwhite')
            fig.set_figwidth(6) 
            ax.set_title('Анализ тональности с помощью алгоритма третьей нейронной сети')
            fig.set_figheight(6)   
            
            plt.savefig(f'Figures/fig_video_{self.id_video}_3')
            
            
            
    def make_WorldCloud_picture(self): 
        
        exist = self.communication.print_comments(self.id_video)
        clear_text = ''
        
        if exist == False:
            print('There are no comments on the video, and we cannot analyze it at the moment')
        
        else:
            for comment in exist:
                comment_text = comment[1]
                clear_text += self.lead_to_initial_form(comment_text)
            self.subs.get_WordCloud(clear_text)
           
        
    def analysis_of_comments_for_a_single_video(self):
        actuality = self.communication.check_actuality_by_id(self.id_video)
        massive_comments = []
        if actuality == False:
            
            try:
                self.get_info_about_video()
                self.get_comments_text()

                massive_data = self.communication.print_comments(self.id_video)

                for comments in massive_data:
                    massive_comments.append(comments[1])

                self.sentiment_eng_analysis(massive_comments)
                self.sentiment_rus_analysis(massive_comments)
                self.sentiment_dost_analysis(massive_comments)

                self.write_to_the_database()
                
                self.analysis_string = ''
                
                               
            except:
                 print('There are no comments on the video, and we cannot analyze it at the moment')
            
        else:
            pass
        
        video = self.communication.extract_obj_by_id(self.id_video)
        
        relation = video[0][7].replace('\n', '\n')
        video_description = video[0][11].replace('\n', '\n')
        
        video_info = f"""
    
ID видеоролика: {video[0][0]}
Название канала: {video[0][1]}
Название видеоролика: {video[0][2]}   
Язык по умолчанию: {video[0][3]}
Количество комментариев: {video[0][4]}
Количество лайков: {video[0][5]}
Количество дизлайков: {video[0][6]}
Соотношение лайков и дизлайков: {relation}
Количество просмотров: {video[0][8]}
Количество tags: {video[0][9]}
Продолжительность видеоролика: {video[0][10]}
Описание видеоролика: 
    
{video_description} """
        
        print(video_info)
        
        analysis = video[0][-2]
        string = analysis.split('-')

        self.get_histogram_for_analyzing_the_tone_of_comments_first_neural_network(float(string[1][1:6]), float(string[2][1:6]))
        self.get_histogram_for_analyzing_the_tone_of_comments_second_neural_network(float(string[3][1:6]), float(string[4][1:6]))
        self.get_histogram_for_analyzing_the_tone_of_comments_third_neural_network(float(string[5][1:6]), float(string[6][1:6]))
        
        string = f"""Точность первой нейронной сети: {self.sentiment['EngModel']}
        Точность второй нейронной сети: {self.sentiment['RusModel']}
        Точность третьей нейронной сети: {self.sentiment['DostModel']}"""
        
        print(string)
            
# #%%
first = FistBranch_actions('https://www.youtube.com/watch?v=YUMDorxFHHQ&t=2s')
# #%%
first.analysis_of_comments_for_a_single_video()
# #%%
first.make_WorldCloud_picture()