from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from service.SocialMediaService import SocialMediaService
from TikTokApi import TikTokApi
import asyncio
import os
import json
import logging
import re
import os
import requests
from model.SocailMediaDataModel import Location, SocialMediaDataModel


log = logging.getLogger(__name__)

class TiktokService(SocialMediaService):
     
    
    def __init__(self) -> None:
        super().__init__()
        pass

    def filter_related_hashtags(self, textExtra) -> list: 
        hashtags = [i['hashtagName'] for i in textExtra]
        return hashtags    

    async def getAnalytics(self, hashtag, max_results) -> SocialMediaDataModel:
        async with TikTokApi() as api:
            output = list()
           # api.browser = await api.playwright.chromium.launch(headless=True, args=["--headless=new"])
            session = await api.create_sessions(ms_tokens=[os.environ.get('MS_TOKEN')], num_sessions=1, sleep_after=3)

            

            log.info(f"Tiktok scraping session estabilished {session} errors found")
            tag = api.hashtag(name=str(hashtag))
            async for video in tag.videos(count=max_results):
                log.info(f"Tiktok Scraping in progress...current count is {len(output)}")
                vid_dict = video.as_dict
                user_model = {}
                post_model = {}
                
                user_model.update({'user_id':vid_dict['author']['uniqueId']})
                user_model.update({'nickname':vid_dict['author']['nickname']})
                user_model.update({'user_bio':vid_dict['author']['signature']})
                user_model.update({'is_user_private':vid_dict['author']['privateAccount']})
                user_model.update({'follower_count':vid_dict['authorStats']['followerCount']})
                user_model.update({'following_count':vid_dict['authorStats']['followingCount']})
                user_model.update({'total_posts':vid_dict['authorStats']['videoCount']})
                user_model.update({'impressions':vid_dict['authorStats']['heartCount']})
                user_model.update({'avatar_link':vid_dict['author']['avatarThumb']})
                user_model.update({'verified':vid_dict['author']['verified']})
                user_model.update({'platform':'Tiktok'})
                
                post_model.update({'caption':vid_dict['desc']})
                post_model.update({'post_id':vid_dict['id']})
                post_model.update({'post_link':f"https://www.tiktok.com/@{vid_dict['author']['uniqueId']}/video/{vid_dict['id']}"})
                post_model.update({'no_of_likes':vid_dict['stats']['diggCount']})
                post_model.update({'no_of_comments':vid_dict['stats']['commentCount']})
                post_model.update({'no_of_shares':vid_dict['stats']['shareCount']})
                post_model.update({'no_of_views':vid_dict['stats']['playCount']})
                post_model.update({'no_of_mentions':vid_dict['stats']['collectCount']})
                post_model.update({'performance':vid_dict['stats']['diggCount']})
                post_model.update({'post_date':vid_dict['createTime']})
                post_model.update({'hashtags':self.filter_related_hashtags(vid_dict['textExtra'])})
                post_model.update({'language':'English'})
                post_model.update({'extra_stats':{}})
                location = self.extract_location(vid_dict['desc'])
                if location is not None:
                    log.info("Tiktok post contains Geolocation data")
                    post_model.update({'location':asyncio.run(await self.extract_geo_location(location))})
                
                user_model.update({'posts':[post_model]})
                output.append(user_model)
        result = SocialMediaDataModel(output)
        log.info(f"Web Scraping Finished for App Name: Tiktok total results {len(output)}")
        return result 