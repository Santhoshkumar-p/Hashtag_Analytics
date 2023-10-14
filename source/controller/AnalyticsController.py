import json
import logging
import os
import pandas as pd
from controller.WebScraperController import WebScraperController
from model.AnalyticsModel import AnalyticsDataModelEncoder
from service.AnalyticsService import AnalyticsService
from model.SocailMediaDataModel import SocialMediaDataModel, SocialMediaDataModelEncoder

log = logging.getLogger(__name__)

class AnalyticsController:

    def __init__(self, hashtag, max_results) -> None:
        self.__hashtag = hashtag
        self.__max_results = max_results
        self.__analytics_service = AnalyticsService()
        self.__env_setup = False
        if self.__env_setup is False:
            self.__env_setup = self.load_environment()
        pass

    def __load_analytics_data(self, hashtag, max_results) -> SocialMediaDataModelEncoder:
        log.info(f'Social Media Data load started for hashtag: {hashtag}')
        #data = app.load_analytics_data(hashtag, max_results)
        data = self.__load_social_media_data(hashtag, max_results)
        log.info(f'Social Media Data load finished for hashtag: {hashtag}')
        return data

    def get_analytics_data(self) -> dict:
        social_media_data = self.__load_analytics_data(self.__hashtag, self.__max_results)
        if social_media_data is not None: 
            log.info(f'Analytics Data load started for hashtag: {self.__hashtag} with data {social_media_data is not None}')
            analytics_data = self.__analytics_service.run_analytics(socialMediaData=social_media_data, keyword=self.__hashtag)
            log.info(f'Analytics Data load finished for hashtag: {self.__hashtag} with data {bool(analytics_data)}')
            output_json = json.dumps(analytics_data,cls=AnalyticsDataModelEncoder,indent = 4)
            with open('./hashtag_analytics_data.json','w') as f:
                 f.write(output_json)
            return analytics_data
        else:
            log.info("Analytics Run Skipped. Social Media data is empty")
            return dict()


    # Load environment variables from .env
    def load_environment(self) -> bool:
        env_setup = False
        with open('./source/.env') as env_file:
            for line in env_file:
                # Remove leading/trailing whitespace and split on '=' to separate key and value
                key, value = map(str.strip, line.strip().split('=', 1))

                # Set the environment variable
                os.environ[key] = value
                env_setup = True
            log.info("[1] Environment file has been loaded")
            return env_setup
    
        

#This App Follows MVC(Model-View-Controller) Architecture 
# if __name__ == "__main__":
#     load_environment()
#     controller = WebScraperController(query='ukraine', max_results=1)
#     result = controller.getSocialMediaTrends()
#     output_json = json.dumps(result, cls=SocialMediaDataModelEncoder, indent = 4)
#     with open('./tiktok_analytics.json','w') as f:
#         f.write(output_json)

    def __load_social_media_data(self, hashtag, max_results) -> SocialMediaDataModel:
        controller = WebScraperController(query=hashtag, max_results=max_results)
        result = controller.getSocialMediaTrends()
        output_json = json.dumps(result, cls=SocialMediaDataModelEncoder, indent = 4)
        with open('./social_media_data.json','w') as f:
            f.write(output_json)
        return result
    


        

