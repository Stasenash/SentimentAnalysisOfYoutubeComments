import SecondBranch
import DB
import Essences

import matplotlib.pyplot as plt

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
        
              
    def get_channel_info(self, channel):
        
        comments = []  
        likes = []
        dislikes = []
        commentsCount = []
        views = []
        list_ids = channel.get_ids_from_video()
        
        for _id in list_ids:
            actuality = self.communication.check_actuality_by_id(_id) 
                  
            if actuality == False:
                
                try:
                    channel.youtube.get_video_info(_id)
                    channel.get_comments_text(_id)                                        
                    channel.write_to_the_database()                    
                    
                    massive_comments = self.communication.print_comments(_id)
                    
                    for comment in massive_comments:
                        comments.append(comment[1])                    
                except:
                    pass
                
            else:
                pass
            
            video = self.communication.extract_obj_by_id(_id)
            
            if video == []:
                pass
            else:
                likes.append(int(video[0][5]))
                dislikes.append(int(video[0][6]))
                commentsCount.append(int(video[0][4]))
                views.append(int(video[0][8]))
                

        basic = Essences.Basic_Information(views, likes, dislikes, commentsCount, comments)
            
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
        
        plt.show()
    
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
        
        plt.show()
        
        
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
        
        plt.show()
    
    
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
        
        plt.show()
    
    def get_histogram_for_analyzing_the_tone_of_comments(self):
        
        pass
            
    
    def comparative_analysis(self):
        
        self.make_objects(self.first_channel, self.second_channel)
        self.get_histogram_by_number_of_views()
        self.get_histogram_for_dislikes()
        self.get_histogram_for_likes()#надо думать какую #надо думать
        self.get_histogram_on_the_number_of_comments() #надо думать какую
        
                
#%%
#fourth = FourthBranch_actions('https://www.youtube.com/user/InokTV', 'https://www.youtube.com/channel/UC2JsSf2SvjCtbZfdgw3MvGg')
##%%
#fourth.comparative_analysis()
















