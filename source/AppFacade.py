from SocailMediaDataModel import SocialMediaDataModel
from SocialMediaService import SocialMediaService
import logging
import asyncio

log = logging.getLogger(__name__)
class AppFacade:

    def __init__(self, query, max_results, socialMediaServices:list) -> None:
        self.query = query
        self.max_results = max_results
        self.services = socialMediaServices
        pass

    def execute(self) -> SocialMediaDataModel:
        log.info('Social Media Analytics Facade has been called')
        result = SocialMediaDataModel()
        for service in self.services:
            service_name = type(service).__name__
            log.info(f"Analytics Stated for App Name:{service_name}")
            analytics_data = asyncio.run(service.getAnalytics(self.query, self.max_results))
            log.info(f"Analytics Finished for App Name: {type(service).__name__} total results {analytics_data.get_no_of_users()}")
            result = analytics_data
        return result
        