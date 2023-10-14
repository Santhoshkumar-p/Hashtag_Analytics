import asyncio
from service.YoutubeService import YoutubeService
from service.InstagramService import InstagramService
from service.WebScraperFacade import WebScraperFacade
from model.SocailMediaDataModel import SocialMediaDataModel
from service.TiktokService import TiktokService
import logging

log = logging.getLogger(__name__)

class WebScraperController: 
    
    def __init__(self,query:str, max_results:int) -> None:
        self.query = query
        self.max_results = max_results
        tiktokService = TiktokService()
        instagramService = InstagramService()
        ytService = YoutubeService()
        # socialMediaServices.append(TwitterService())
        # socialMediaServices.append(SnapchatService())
        self.socialMediaServices = [ytService,instagramService,tiktokService]
        self.appFacade = WebScraperFacade(self.query, self.max_results, socialMediaServices=self.socialMediaServices)
        pass

    def getSocialMediaTrends(self) -> SocialMediaDataModel:       
        log.info("Social Media Analytics App Controller has been called")   
        log.info("Social Media Plaform currently supporting")   
        for platform in self.socialMediaServices:
            service_name = type(platform).__name__
            log.info(f"App Name: {service_name}")
        result = asyncio.run(self.appFacade.execute())
        log.info(f"Social Media Analytics Result Size {result.get_no_of_users()}")  
        return result

