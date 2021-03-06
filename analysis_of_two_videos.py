import analysis_of_one_video
import DB
import Essences

import matplotlib.pyplot as plt
from urllib.parse import urlparse

#%%
class AnalysisOfTwoVideosActions:
    
    def __init__(self, link1, link2):
        
        self.link1 = link1
        self.link2 = link2 
        
        if link1 == link2:
            print('Please enter two different links so that we can perform the analysis')
            
        else:
            self.first_video = analysis_of_one_video.AnalysisOfOneVideoActions(link1)
            self.second_video = analysis_of_one_video.AnalysisOfOneVideoActions(link2)
                        
        try:
            video_database = DB.Video_DB('VideoDatabase')
            self.communication = DB.Interaction(video_database)
            self.communication.create_table('Videoclips')
            self.communication.create_table_for_comments()
        except:
            pass
        
        self.x = ['первое видео', 'второе видео']
        
        
    def _parse_url_path(self, url):
        
        array = urlparse(url)
        return array.path


    def _parse_url_query(self, url):
        
        array = urlparse(url)
        query = array.query
        query_parts = query.split('&')
        params = {}
        for param in query_parts:
            item = param.split('=')
            if not item[1]:
                params[item[0]] = ''
            else:
                params[item[0]] = item[1]

        return params
            
            
    def parse_vid_from_url(self, youtube_url):

        if 'youtube.com' in youtube_url:
            params = self._parse_url_query(youtube_url)
            return params['v']
        elif 'youtu.be' in youtube_url:
            path = self._parse_url_path(youtube_url)
            vid = path[1:]
            return vid
        else:
            raise Exception('The supplied URL does not look like a Youtube URL')
        
    
    def get_info_about_video(self, youtube_video, video_id):
        
        comments=[]
        actuality = self.communication.check_actuality_by_id(video_id)
        
        if actuality == False: 
            
            youtube_video.get_info_about_video()            
            youtube_video.get_comments_text() 
            
            comments_massive = self.communication.print_comments(video_id)
            
            for comment in comments_massive:
                comments.append(comment[1])
            
            youtube_video.sentiment_eng_analysis(comments)
            youtube_video.sentiment_rus_analysis(comments)
            youtube_video.sentiment_dost_analysis(comments)
               
            youtube_video.write_to_the_database()
            
            youtube_video.analysis_string = ''


        else:
            pass
        
        video = self.communication.extract_obj_by_id(video_id)
        viewsCount = int(video[0][8])
        likesCount = int(video[0][5])
        dislikesCount = int(video[0][6])
        commentsCount = int(video[0][4])
        analysis = video[0][-2]

        basic = Essences.Basic_Information(viewsCount, likesCount, dislikesCount, commentsCount, comments, analysis) 
            
        return basic
         
    
    def make_objects(self, obj1, obj2):
        self.one = self.get_info_about_video(obj1, self.parse_vid_from_url(self.link1))
        self.two = self.get_info_about_video(obj2, self.parse_vid_from_url(self.link2))     
        
    
    def get_histogram_for_analyzing_the_tone_of_comments_first_neural_network(self):
        
        string1 = self.one.analysis.split("-")
        string2 = self.two.analysis.split("-")
        
        x1 = ['positive_1', 'positive_2']
        x2 = ['negative_1', 'negative_2']
        y1 = [float(string1[1][1:5]), float(string2[1][1:5])]
        y2 = [float(string1[2][1:5]), float(string2[2][1:5])]
        
        fig, ax = plt.subplots()

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью первого алгоритма нейронной сети')
        fig.set_facecolor('floralwhite')
        plt.savefig(f'Figures/fig_video_comparison_1')
        
        
    def get_histogram_for_analyzing_the_tone_of_comments_second_neural_network(self):
        
        string1 = self.one.analysis.split("-")
        string2 = self.two.analysis.split("-")
        
        x1 = ['positive_1', 'positive_2']
        x2 = ['negative_1', 'negative_2']
        y1 = [float(string1[3][1:5]), float(string2[3][1:5])]
        y2 = [float(string1[4][1:5]), float(string2[4][1:5])]
        
        fig, ax = plt.subplots()

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью второго алгоритма нейронной сети')
        fig.set_facecolor('floralwhite')
        plt.savefig(f'Figures/fig_video_comparison_2')
        
        
    def get_histogram_for_analyzing_the_tone_of_comments_third_neural_network(self):
        
        string1 = self.one.analysis.split("-")
        string2 = self.two.analysis.split("-")
        
        x1 = ['positive_1', 'positive_2']
        x2 = ['negative_1', 'negative_2']
        y1 = [float(string1[5][1:5]), float(string2[5][1:5])]
        y2 = [float(string1[6][1:5]), float(string2[6][1:5])]
        
        fig, ax = plt.subplots()

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью третьего алгоритма нейронной сети')
        fig.set_facecolor('floralwhite')
        plt.savefig(f'Figures/fig_video_comparison_3')
        
        
    def get_histogram_by_number_of_views(self):
        
        y = [self.one.views, self.two.views]
        
        fig, ax = plt.subplots()

        ax.bar(self.x, y, width = 0.15)

        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(6) 
        ax.set_title('Сравнительная гистограмма по количеству просмотров')
        fig.set_figheight(6)   
        
        plt.savefig(f'Figures/fig_video_comparison_4')
    
    def get_histogram_for_likes_and_dislikes(self):
        x1 = ['Likes_1', 'Likes_2']
        x2 = ['Dislikes_1', 'Dislikes_2']
        y1 = [self.one.likes, self.two.likes]
        y2 = [self.one.dislikes, self.two.dislikes]
        
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по лайкам и дизлайкам')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_video_comparison_5')
    
    def get_histogram_on_the_number_of_comments(self):
        
        y = [self.one.comments_quantity, self.two.comments_quantity]
        
        fig, ax = plt.subplots()

        ax.bar(self.x, y, width = 0.15)

        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(6) 
        ax.set_title('Сравнительная гистограмма по количеству комментариев')
        fig.set_figheight(6)   
        
        plt.savefig(f'Figures/fig_video_comparison_6')
            
    
    def comparative_analysis(self):
        
        self.make_objects(self.first_video, self.second_video)
        self.get_histogram_by_number_of_views() 
        self.get_histogram_for_likes_and_dislikes() 
        self.get_histogram_on_the_number_of_comments() 
        self.get_histogram_for_analyzing_the_tone_of_comments_first_neural_network()
        self.get_histogram_for_analyzing_the_tone_of_comments_second_neural_network()
        self.get_histogram_for_analyzing_the_tone_of_comments_third_neural_network()
# #%%
# third = AnalysisOfTwoVideosActions('https://www.youtube.com/watch?v=YUMDorxFHHQ&t=2s', 'https://www.youtube.com/watch?v=lrS7H0eqYww')
# #%%
# third.comparative_analysis()