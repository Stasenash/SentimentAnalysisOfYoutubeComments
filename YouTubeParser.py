import json
import urllib.parse as urlbpar
import urllib.request as urlb
import isodate
import datetime 
import Additionally
from langdetect import detect 

from urllib.parse import urlparse
#import urllib2.request
#from urlparse import urlparse
#import urllib
#import urllib2
#%%

class YouTubeAPI:

    apis = {
        'videos.list': 'https://www.googleapis.com/youtube/v3/videos',
        'search.list': 'https://www.googleapis.com/youtube/v3/search',
        'channels.list': 'https://www.googleapis.com/youtube/v3/channels',
        'playlists.list': 'https://www.googleapis.com/youtube/v3/playlists',
        'playlistItems.list': 'https://www.googleapis.com/youtube/v3/playlistItems',
        'activities': 'https://www.googleapis.com/youtube/v3/activities',
    }

    page_info = {}
    
    def __init__(self):
                    
        self.youtube_key = 'AIzaSyAbzkiIwa0SA176y6ZaOgqko1uo-lLWuA0'
        
        
    def convert_time(self, value):

         if isinstance(value, datetime.timedelta):
             return isodate.duration_isoformat(value)
         
         if isinstance(value, (int, float)):
             return isodate.duration_isoformat(
                 datetime.timedelta(seconds=value)
            )
        
         if isinstance(value, str):
            return f'{value[2:4]}:{value[5:7]}'
             
         else:
             raise Exception("Invalid duration value and type")
    
    
    def convert_date(self, value):
        return f'{value[:10]}'
        
    
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
            
            
    def get_api(self, name): #возвращает ссылку из словаря apis
        return self.apis[name]
    
    
    def api_get(self, url, parameters):

        parameters['key'] = self.youtube_key

        file = urlb.urlopen(url + "?" + urlbpar.urlencode(parameters))
        data = file.read()
        file.close()

        return data
    
    
    def decode_single(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array[0]
            
            
    def decode_list(self, api_data):

        res_obj = json.loads(api_data)
        if 'error' in res_obj:
            msg = "Error " + res_obj['error']['code'] + " " + res_obj['error']['message']
            if res_obj['error']['errors'][0]:
                msg = msg + " : " + res_obj['error']['errors'][0]['reason']
            raise Exception(msg)
        else:
            self.page_info = {
                'resultsPerPage': res_obj['pageInfo']['resultsPerPage'],
                'totalResults': res_obj['pageInfo']['totalResults'],
                'kind': res_obj['kind'],
                'etag': res_obj['etag'],
                'prevPageToken': None,
                'nextPageToken': None
            }
            if 'prevPageToken' in res_obj:
                self.page_info['prevPageToken'] = res_obj['prevPageToken']
            if 'nextPageToken' in res_obj:
                self.page_info['nextPageToken'] = res_obj['nextPageToken']

            items_array = res_obj['items']
            if isinstance(items_array, dict) or len(items_array) == 0:
                return False
            else:
                return items_array

                    
    def get_channel_by_name(self, username, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'forUsername': username,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)
       

    def get_channel_by_id(self, id, optional_params=False):

        api_url = self.get_api('channels.list')
        params = {
            'id': id,
            'part': 'id,snippet,contentDetails,statistics,invideoPromotion'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_single(api_data)
    
    
    def get_playlists_by_channel_id(self, channel_id, optional_params={}):

        api_url = self.get_api('playlists.list')
        params = {
            'channelId': channel_id,
            'part': 'id, snippet, status'
        }
        if optional_params:
            params += optional_params

        api_data = self.api_get(api_url, params)
        return self.decode_list(api_data)


    def get_playlist_items_by_playlist_id(self, playlist_id, max_results=50):

        api_url = self.get_api('playlistItems.list')
        params = {
            'playlistId': playlist_id,
            'part': 'id, snippet, contentDetails, status',
            'maxResults': max_results
        }
        api_data = self.api_get(api_url, params)
        return self.decode_list(api_data)
    
    
    def download_channel_videos(self, channel_url):
        
        info_about_all_video = []
        channel_id = self.get_channel_from_url(channel_url)['id']
        playlists = self.get_playlists_by_channel_id(channel_id)
        
        for playlist in playlists:
            playlist_id = playlist['id']           
            items = self.get_playlist_items_by_playlist_id(playlist_id)
            info_about_all_video.append(items)
        
        return info_about_all_video
     
        
    def in_dictionary(self, key, dictionary):
        if key in dictionary.keys():
            return True
        return False


    def get_video_info(self, id_video):
                
        self.video_subs = Additionally.GetDescryption()
        
        api_url = self.get_api('videos.list')
        parameters = {
            'id': id_video,
            'key': self.youtube_key,
            'part': 'id, snippet, contentDetails, player, statistics, status'
        }
        apiData = self.api_get(api_url, parameters)
        
        self.all_info = self.decode_single(apiData)
        
        self.commentsCount = self.in_dictionary('commentCount', self.all_info['statistics'])
        
        if self.commentsCount == True:
        
            video_duration = self.all_info['contentDetails']['duration']
            self.all_info['contentDetails']['duration'] = self.convert_time(video_duration)
            
            video_description = self.all_info['snippet']['description']
            self.all_info['snippet']['description'] = video_description.replace('\n', '\n') 
            
            
            self.video_subs.get_clear_text(id_video)
            
            if self.video_subs.flag:
                self.language = detect(self.video_subs.clear_text)
            else:
                self.language = ' Sorry, there are no subtitles for the video, we cannot clearly identify the language'
        
        else:
            raise Exception
        
        return self.all_info
       
    
    def get_channel_from_url(self, youtube_url):

        if 'youtube.com' not in youtube_url:
            raise Exception('The supplied URL does not look like a Youtube URL')
        path = self._parse_url_path(youtube_url)
        if '/channel' in path:
            segments = path.split('/')
            channel_id = segments[len(segments) - 1]
            self.channel = self.get_channel_by_id(channel_id)
        elif '/user' in path:
            segments = path.split('/')
            username = segments[len(segments) - 1]
            self.channel = self.get_channel_by_name(username)           
        else:
            raise Exception('The supplied URL does not look like a Youtube Channel URL')

        return self.channel
        


