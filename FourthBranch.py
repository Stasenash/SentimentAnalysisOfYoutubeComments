import SecondBranch
import DB
import Essences

import matplotlib.pyplot as plt
from data_analyzer import DataAnalyzer
#%%
class FourthBranch_actions:
    
    def __init__(self, link1, link2):

        self.link1 = link1
        self.link2 = link2 
        
        if link1 == link2:
            print('Please enter two different links so that we can perform the analysis')
            
        else:
            self.first_channel = SecondBranch.SecondBranch_actions(link1)
            self.second_channel = SecondBranch.SecondBranch_actions(link2)
                        
        try:
            video_database = DB.Video_DB('VideoDatabase')
            self.communication = DB.Interaction(video_database)
            self.communication.create_table('Videoclips')
            self.communication.create_table_for_comments()
        except:
            pass
    
    #
    # def sentiment_eng_analysis(self, massive_comments):
    #
    #     if massive_comments == False:
    #         return 'There are no comments on the video, and we cannot analyze it at the moment'
    #     else:
    #
    #         analysis_dictionary = DataAnalyzer.get_eng_analysis(massive_comments)
    #         self.analysis_string += f"Анализ первой(положительные) - {analysis_dictionary['positive']}, анализ первой(негативные) - {analysis_dictionary['negative']}"
    #
    #
    #
    # def sentiment_rus_analysis(self, massive_comments):
    #
    #     if massive_comments == False:
    #         return 'There are no comments on the video, and we cannot analyze it at the moment'
    #     else:
    #
    #         analysis_dictionary = DataAnalyzer.get_rus_analysis(massive_comments)
    #         self.analysis_string += f"Анализ второй(положительные) - {analysis_dictionary['positive']}, анализ второй(негативные) - {analysis_dictionary['negative']}"
    #
    #
    #
    # def sentiment_dost_analysis(self, massive_comments):
    #
    #     if massive_comments == False:
    #         return 'There are no comments on the video, and we cannot analyze it at the moment'
    #     else:
    #         analysis_dictionary = DataAnalyzer.get_rus_analysis(massive_comments)
    #         self.analysis_string += f"Анализ третьей(положительные) - {analysis_dictionary['positive']}, анализ третьей(негативные) - {analysis_dictionary['negative']}"
    #
    #
    def get_channel_info(self, channel):
        
        comments = []  
        likes = []
        dislikes = []
        commentsCount = []
        views = []
        analysis = []
        massive_pos_1 = []
        massive_neg_1 = []
        massive_pos_2 = []
        massive_neg_2 = []
        massive_pos_3 = []
        massive_neg_3 = []
        self.massive_channel_sentiment = []
        list_ids = channel.get_ids_from_video()
        if not list_ids:
            print('Channel has not got a playlists')
        else:
            for _id in list_ids:
                actuality = self.communication.check_actuality_by_id(_id)
                if actuality == False:

                    try:
                        channel.youtube.get_video_info(_id)
                        channel.get_comments_text(_id)

                        massive_comments = self.communication.print_comments(_id)

                        for comment in massive_comments:
                            comments.append(comment[1])

                        channel.sentiment_eng_analysis(comments)
                        channel.sentiment_rus_analysis(comments)
                        channel.sentiment_dost_analysis(comments)

                        channel.write_to_the_database()
                        channel.analysis_string = ''

                    except:
                        pass

                else:
                    pass

                try:
                    video = self.communication.extract_obj_by_id(_id)


                    likes.append(int(video[0][5]))
                    dislikes.append(int(video[0][6]))
                    commentsCount.append(int(video[0][4]))
                    views.append(int(video[0][8]))
                    analysis_comments = video[0][-2]
                    analysis.append(analysis_comments)

                    string = analysis_comments.split('-')

                    massive_pos_1.append(float(string[1][1:6]))
                    massive_neg_1.append(float(string[2][1:6]))
                    massive_pos_2.append(float(string[3][1:6]))
                    massive_neg_2.append(float(string[4][1:6]))
                    massive_pos_3.append(float(string[5][1:6]))
                    massive_neg_3.append(float(string[6][1:6]))
                except:
                    pass
            try:
                self.massive_channel_sentiment.append(massive_pos_1)
                self.massive_channel_sentiment.append(massive_neg_1)
                self.massive_channel_sentiment.append(massive_pos_2)
                self.massive_channel_sentiment.append(massive_neg_2)
                self.massive_channel_sentiment.append(massive_pos_3)
                self.massive_channel_sentiment.append(massive_neg_3)
            except:
                pass
        
        basic = Essences.Basic_Information(views, likes, dislikes, commentsCount, comments, analysis)
            
        return basic


    def make_objects(self, obj1, obj2):
        self.one = self.get_channel_info(obj1)
        self.two = self.get_channel_info(obj2)   
        
    
    def get_histogram_by_number_of_views(self):
        
        x1 = ['Max_views_1', 'Max_views_2']
        x2 = ['Min_views_1', 'Min_views_2']
        y1 = [max(self.one.views), max(self.two.views)]
        y2 = [min(self.one.views), min(self.two.views)]
        
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по максимальному и минимальному количеству просмотров')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_1')
    
    
    def get_histogram_for_dislikes(self):
        
        x1 = ['Max_dislikes_1', 'Max_dislikes_2']
        x2 = ['Min_dislikes_1', 'Min_dislikes_2']
        y1 = [max(self.one.dislikes), max(self.two.dislikes)]
        y2 = [min(self.one.dislikes), min(self.two.dislikes)]
        
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по максимальному и минимальному количеству дизлайков')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_2')
        
        
    def get_histogram_for_likes(self):
        
        x1 = ['Max_likes_1', 'Max_likes_2']
        x2 = ['Min_likes_1', 'Min_likes_2']
        y1 = [max(self.one.likes), max(self.two.likes)]
        y2 = [min(self.one.likes), min(self.two.likes)]
        
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по максимальному и минимальному количеству лайков')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_3')
    
    
    def get_histogram_on_the_number_of_comments(self):
        
        x1 = ['Max_com_1', 'Max_com_2']
        x2 = ['Min_com_1', 'Min_com_2']
        y1 = [max(self.one.comments_quantity), max(self.two.comments_quantity)]
        y2 = [min(self.one.comments_quantity), min(self.two.comments_quantity)]
        
        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по максимальному и минимальному количеству комментариев')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_4')
    
    
    def get_histogram_for_analyzing_the_tone_of_comments_first_neural_network(self, massive_pos_1, massive_neg_1, massive_pos_2, massive_neg_2):
        
        x1=['positive_1', 'positive_2']
        x2=['negative_1', 'negative_2']        
        y1 = [sum(massive_pos_1)/(len(massive_pos_1)), sum(massive_pos_2)/len(massive_pos_2)]
        y2 = [sum(massive_neg_1)/len(massive_neg_1), sum(massive_neg_2)/len(massive_neg_2)]  

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью алгоритма первой нейронной сети')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_5')
    
    
    def get_histogram_for_analyzing_the_tone_of_comments_second_neural_network(self, massive_pos_1, massive_neg_1, massive_pos_2, massive_neg_2):
        
        x1=['positive_1', 'positive_2']
        x2=['negative_1', 'negative_2']        
        y1 = [sum(massive_pos_1)/(len(massive_pos_1)), sum(massive_pos_2)/len(massive_pos_2)]
        y2 = [sum(massive_neg_1)/len(massive_neg_1), sum(massive_neg_2)/len(massive_neg_2)]  

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью алгоритма второй нейронной сети')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_6')
    
    
    def get_histogram_for_analyzing_the_tone_of_comments_third_neural_network(self, massive_pos_1, massive_neg_1, massive_pos_2, massive_neg_2):
        
        x1=['positive_1', 'positive_2']
        x2=['negative_1', 'negative_2']        
        y1 = [sum(massive_pos_1)/(len(massive_pos_1)), sum(massive_pos_2)/len(massive_pos_2)]
        y2 = [sum(massive_neg_1)/len(massive_neg_1), sum(massive_neg_2)/len(massive_neg_2)]  

        fig, ax = plt.subplots()

        ax.bar(x1, y1, width = 0.4)
        ax.bar(x2, y2, width = 0.4)
        
        ax.set_facecolor('seashell')
        fig.set_figwidth(6)    
        fig.set_figheight(6)   
        ax.set_title('Сравнительная гистограмма по анализу тональности с помощью алгоритма третьей нейронной сети')
        fig.set_facecolor('floralwhite')
        
        plt.savefig(f'Figures/fig_channel_comparison_7')
        
        
    def comparative_analysis(self):
        
        self.make_objects(self.first_channel, self.second_channel)
        self.get_histogram_by_number_of_views()
        self.get_histogram_for_dislikes()
        self.get_histogram_for_likes()#надо думать какую #надо думать
        self.get_histogram_on_the_number_of_comments() #надо думать какую
        self.get_histogram_for_analyzing_the_tone_of_comments_first_neural_network(self.massive_channel_sentiment[0], self.massive_channel_sentiment[1], self.massive_channel_sentiment[6], self.massive_channel_sentiment[7])
        self.get_histogram_for_analyzing_the_tone_of_comments_second_neural_network(self.massive_channel_sentiment[2], self.massive_channel_sentiment[3], self.massive_channel_sentiment[8], self.massive_channel_sentiment[9])
        self.get_histogram_for_analyzing_the_tone_of_comments_third_neural_network(self.massive_channel_sentiment[4], self.massive_channel_sentiment[5], self.massive_channel_sentiment[10], self.massive_channel_sentiment[11])
        
                
#%%
fourth = FourthBranch_actions('https://www.youtube.com/user/InokTV', 'https://www.youtube.com/channel/UC9FSprjbRqHtsfxbxVO_JWA')
##%%
fourth.comparative_analysis()
















