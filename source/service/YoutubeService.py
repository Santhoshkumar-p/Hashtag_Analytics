import asyncio
from datetime import datetime
import logging
import os
import requests
from model.SocailMediaDataModel import SocialMediaDataModel

from service.SocialMediaService import SocialMediaService

log = logging.getLogger(__name__)

class YoutubeService(SocialMediaService):
    
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def __init__(self) -> None:
        self.__key = os.environ.get('YT_KEY').strip('\'')
        super().__init__()

    
    def search_videos(self, hashtag, max_results):
        search_url = f"{self.BASE_URL}search"
        params = {
            'part': 'snippet',
            'q': hashtag,
            'type': 'video',
            'maxResults': max_results,
            'key': self.__key
        }
        response = requests.get(search_url, params=params)
        log.info('Youtube Search Query API Call Responded')
        return response.json()

    def get_video_details(self, video_id):
        videos_url = f"{self.BASE_URL}videos"
        params = {
            'part': 'snippet,statistics',
            'id': video_id,
            'key': self.__key
        }
        response = requests.get(videos_url, params=params)
        log.info('Youtube Video Query API Call Responded')
        return response.json()

    def get_channel_details(self, channel_id):
        channels_url = f"{self.BASE_URL}channels"
        params = {
            'part': 'snippet,statistics',
            'id': channel_id,
            'key': self.__key
        }
        response = requests.get(channels_url, params=params)
        log.info('Youtube Channel Query API Call responded')
        return response.json()
    
    async def getAnalytics(self, hashtag, max_results) -> SocialMediaDataModel:
        #Due to API rate limiting we are decreasing count to 10 percent
        search_data = self.search_videos(hashtag, max_results=int(max_results*0.20))
        output = []
        for item in search_data['items']:
            video_id = item['id']['videoId']
            video_details = self.get_video_details(video_id)
            channel_id = video_details['items'][0]['snippet']['channelId']
            channel_data = self.get_channel_details(channel_id)
            post_model ={}
            user_model ={}
            if 'items' in video_details and 'items' in channel_data:
                post_model.update({'caption': video_details['items'][0]['snippet']['title']})
                post_model.update({'post_id': video_id})
                post_model.update({'post_link': f'https://www.youtube.com/watch?v={video_id}'})
                post_model.update({'no_of_likes': int(video_details['items'][0]['statistics'].get('likeCount',0))})
                post_model.update({'no_of_comments': int(video_details['items'][0]['statistics'].get('commentCount',0))})
                post_model.update({'no_of_shares':0})
                post_model.update({'no_of_views':int(video_details['items'][0]['statistics'].get('viewCount',0))})
                post_model.update({'no_of_mentions':0})
                post_model.update({'performance':0})
                date_obj = datetime.strptime(video_details['items'][0]['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
                post_model.update({'post_date': int(date_obj.timestamp())})
                post_model.update({'hashtags':[]})
                post_model.update({'language':'English'})
                post_model.update({'extra_stats':{}})
                location = self.extract_location(video_details['items'][0]['snippet']['title'])
                if location is not None:
                    log.info("Youtube post contains Geolocation data")
                    post_model.update({'location':asyncio.run(await self.extract_geo_location(location))})
                    
                user_model.update({'user_id': channel_id})
                user_model.update({'nickname': channel_data['items'][0]['snippet']['title']})
                user_model.update({'user_bio':channel_data['items'][0]['snippet']['description']})
                user_model.update({'is_user_private':False})
                user_model.update({'follower_count':int(channel_data['items'][0]['statistics'].get('subscriberCount',0))})
                user_model.update({'following_count':0})
                user_model.update({'total_posts':int(channel_data['items'][0]['statistics'].get('videoCount',0))})
                user_model.update({'impressions':0})
                user_model.update({'avatar_link':channel_data['items'][0]['snippet']['thumbnails']['default']['url']})
                user_model.update({'verified': channel_data['items'][0]['snippet']['thumbnails'].get('verified', False)})
                user_model.update({'platform':'Youtube'})
                user_model.update({'posts':[post_model]})
                output.append(user_model)

        log.info(f"Youtube keyword/hashtag scrapping is completed with count {len(output)}") 
        result = SocialMediaDataModel(output)
        return result
