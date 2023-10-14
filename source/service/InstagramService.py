import asyncio
from datetime import datetime
import logging
import os
from apify_client import ApifyClient
from model.SocailMediaDataModel import SocialMediaDataModel

from service.SocialMediaService import SocialMediaService


log = logging.getLogger(__name__)

class InstagramService(SocialMediaService):
    
    INSTGRAM_SCRAPPING_URL = "apify/instagram-hashtag-scraper"
    

    def __init__(self) -> None:
        super().__init__()
        self.__key = str(os.environ.get('INSTA_API_KEY')).strip('\'')
        self.__client = ApifyClient(self.__key)
        pass
    
    async def getAnalytics(self, hashtag, max_results) -> SocialMediaDataModel:
        output = []
        post_model ={}
        user_model ={}
        run_input_hashtags = {
            "hashtags": [hashtag],
            "resultsLimit": max_results,
        }
        run_hashtags = self.__client.actor(self.INSTGRAM_SCRAPPING_URL).call(run_input=run_input_hashtags)
        for item in self.__client.dataset(run_hashtags["defaultDatasetId"]).iterate_items():
            post_model.update({'caption': item['caption']})
            post_model.update({'post_id': item['id']})
            post_model.update({'post_link': item['url']})
            post_model.update({'no_of_likes': item['likesCount']})
            post_model.update({'no_of_comments': item['commentsCount']})
            post_model.update({'no_of_shares':0})
            post_model.update({'no_of_views':0})
            post_model.update({'no_of_mentions':0})
            post_model.update({'performance':0})
            date_obj = datetime.strptime(item['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ")
            post_model.update({'post_date': int(date_obj.timestamp())})
            post_model.update({'hashtags':item['hashtags']})
            post_model.update({'language':'English'})
            post_model.update({'extra_stats':{}})
            location = self.extract_location(item['caption'])
            if location is not None:
                log.info("Instagram post contains Geolocation data")
                post_model.update({'location':asyncio.run(await self.extract_geo_location(location))})
                
            user_model.update({'user_id': item['ownerId']})
            user_model.update({'nickname': item['ownerUsername']})
    
            run_input_usernames = {"usernames":[item['ownerUsername']]}
            run_usernames = self.__client.actor("apify/instagram-profile-scraper").call(run_input=run_input_usernames)
            for useritem in self.__client.dataset(run_usernames["defaultDatasetId"]).iterate_items():
                user_model.update({'user_bio':useritem['biography']})
                user_model.update({'is_user_private':useritem['private']})
                user_model.update({'follower_count':useritem['followersCount']})
                user_model.update({'following_count':useritem['followsCount']})
                user_model.update({'total_posts':useritem['highlightReelCount']})
                user_model.update({'impressions':useritem['highlightReelCount']})
                user_model.update({'avatar_link':useritem['url']})
                user_model.update({'verified':useritem['verified']})
                user_model.update({'platform':'Instagram'})
            user_model.update({'posts':[post_model]})
            output.append(user_model)
        log.info(f"Instagram Hashtag Scrapping is completed with count {len(output)}")
        result = SocialMediaDataModel(output)
        return result
