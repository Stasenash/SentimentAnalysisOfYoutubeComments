import Additionally
from urllib.parse import urlparse

#%%
class BlogersWordcloudActions:
    
    def __init__(self, link):
        
        self.link = link
        self.wordcloud_picture = Additionally.GetDescryption()
        
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
            
            
    def get_wordcloud_picture(self):
        
        video_id = self.parse_vid_from_url(self.link)
        
        try:
            self.wordcloud_picture.get_clear_text(video_id)
            text = self.wordcloud_picture.clear_text
            
            self.wordcloud_picture.get_WordCloud(text)
        except:
            print('We cannot plot a chart because there are no subtitles for the video')
        
#%%
#fifth = FifthBranch_actions('https://www.youtube.com/watch?v=banxElYv490')
#fifth.get_wordcloud_picture()