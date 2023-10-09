from AppFacade import AppFacade
from SocailMediaDataModel import SocialMediaDataModel
from TiktokService import TiktokService
import logging

log = logging.getLogger(__name__)

class AppController: 
    def __init__(self,query:str, max_results:int) -> None:
        self.query = query
        self.max_results = max_results
        tiktokService = TiktokService()
        # socialMediaServices.append(YoutubeService())
        # socialMediaServices.append(InstagramService())
        # socialMediaServices.append(TwitterService())
        # socialMediaServices.append(SnapchatService())
        self.socialMediaServices = [tiktokService]
        self.appFacade = AppFacade(self.query, self.max_results, socialMediaServices=self.socialMediaServices)
        pass

    def getSocialMediaTrends(self) -> SocialMediaDataModel:       
        log.info("Social Media Analytics App Controller has been called")   
        log.info("Social Media Plaform currently supporting")   
        for platform in self.socialMediaServices:
            service_name = type(platform).__name__
            log.info(f"App Name: {service_name}")
        result = self.appFacade.execute()
        log.info(f"Social Media Analytics Result Size {result.get_no_of_users()}")  
        return result

