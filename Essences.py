class Video:
    
    def __init__(self, video_id, channel_name, 
                 video_name, language, comment_count, 
                 like_count, dislike_count, relation, views_count,
                 tags_count, video_duration, video_discription, analysis):
        
        self.video_id = video_id
        self.channel_name = channel_name
        self.video_name = video_name       
        self.language = language
        self.comment_count = comment_count
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.relation = relation
        self.views_count = views_count
        self.tags_count = tags_count
        self.video_duration = video_duration
        self.video_discription = video_discription
        self.analysis = analysis
        
        
    def __str__(self):
        
        return f"""
    ID видеоролика: {self.video_id}
    Название канала: {self.channel_name}
    Название видеоролика: {self.video_name}  
    Язык по умолчанию: {self.language}
    Количество комментариев: {self.comment_count}
    Количество лайков: {self.like_count}
    Количество дизлайков: {self.dislike_count}
    Соотношение лайков и дизлайков: self.relation
    Количество просмотров: {self.views_count}
    Количество tags: {self.tags_count}
    Продолжительность видеоролика: {self.video_duration}
    Описание видеоролика: 
        
{self.video_discription}
    
    """
        
#%%
class Basic_Information:
    
    def __init__(self, views, likes, dislikes, comments_quantity, comments, analysis):
        
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.comments_quantity = comments_quantity
        self.comments = comments
        self.analysis = analysis
        

