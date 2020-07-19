#from selenium import webdriver
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
import pymorphy2
from tqdm import tqdm
import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude
from wordcloud import WordCloud, ImageColorGenerator
import random

#%%

class GetDescryption():
    
    def __init__(self):
        self.stopwords = ['это', 'еще', 'ещё', 'и', 'в', 'во', 'не', 'что', 'он', 'на', 'я', 'с', 'со', 'как', 'а', 'то', 'все', 'она', 'так', 'его', 'но', 'да', 'ты', 'к', 'у', 'же', 'вы', 'за', 'бы', 'по', 'только', 'ее', 'мне', 'было', 'вот', 'от', 'меня', 'еще', 'нет', 'о', 'из', 'ему', 'теперь', 'когда', 'даже', 'ну', 'вдруг', 'ли', 'если', 'уже', 'или', 'ни', 'быть', 'был', 'него', 'до', 'вас', 'нибудь', 'опять', 'уж', 'вам', 'ведь', 'там', 'потом', 'себя', 'ничего', 'ей', 'может', 'они', 'тут', 'где', 'есть', 'надо', 'ней', 'для', 'мы', 'тебя', 'их', 'чем', 'была', 'сам', 'чтоб', 'без', 'будто', 'чего', 'раз', 'тоже', 'себе', 'под', 'будет', 'ж', 'тогда', 'кто', 'этот', 'того', 'потому', 'этого', 'какой', 'совсем', 'ним', 'здесь', 'этом', 'один', 'почти', 'мой', 'тем', 'чтобы', 'нее', 'сейчас', 'были', 'куда', 'зачем', 'всех', 'никогда', 'можно', 'при', 'наконец', 'два', 'об', 'другой', 'хоть', 'после', 'над', 'больше', 'тот', 'через', 'эти', 'нас', 'про', 'всего', 'них', 'какая', 'много', 'разве', 'три', 'эту', 'моя', 'впрочем', 'хорошо', 'свою', 'этой', 'перед', 'иногда', 'лучше', 'чуть', 'том', 'нельзя', 'такой', 'им', 'более', 'всегда', 'конечно', 'всю', 'между']
        self.morph = pymorphy2.MorphAnalyzer()
        self.pictures = ['crocodile_picture.png', 'dog_picture.png', 'parrot_picture.png', 'unicorn_picture.png', 'rabbit_picture.png']
        self.flag = True
                  
        
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
    
      
    def get_descryption(self, video_id):
               
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        except:
            transcript_list = 'Not Found'
            
        if transcript_list == 'Not Found':
            transcript = 'Not Found'
        else:
            try:
                transcript = transcript_list.find_generated_transcript(['ru', 'en'])
            except:
                transcript =  transcript_list.find_manually_created_transcript(['ru',  'en']) 
            
        try:
            result = transcript.fetch()
        except:
            result = False
            self.flag = False
            
        return result
    
    
    def get_clear_text(self, _id):
        
        list_of_dictionaries = self.get_descryption(_id)
        

        if self.flag == True:
        
            text_var = ''
            
            for i in list_of_dictionaries:
                if i['text'].startswith('['):
                    pass
                else:
                    text_var += i['text'] + ' '
                    
            self.clear_text = self.lead_to_initial_form(text_var)


        
    def get_WordCloud(self, string): 
        
        if self.flag == True:
            d = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
            
            text = string
            
            random_picture = random.choice(self.pictures)
            picture_color = np.array(Image.open(os.path.join(d, random_picture)))
            
            picture_color = picture_color[::3, ::3]
            
            picture_mask = picture_color.copy()
            picture_mask[picture_mask.sum(axis=2) == 0] = 255
            
            edges = np.mean([gaussian_gradient_magnitude(picture_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
            picture_mask[edges > .08] = 255
            
            wc = WordCloud(max_words=2000, mask=picture_mask, max_font_size=40, random_state=42, relative_scaling=0)
            
            wc.generate(text)
            plt.imshow(wc)
            
            # create coloring from image
            image_colors = ImageColorGenerator(picture_color)
            wc.recolor(color_func=image_colors)
            plt.figure(figsize=(10, 10))
            plt.title('Most common words')
            plt.imshow(wc, interpolation="bilinear")
            wc.to_file("Figures/picture_new.png")

        else:
            print('We cannot plot a chart because there are no subtitles for the video')
            
    
    

        
        


