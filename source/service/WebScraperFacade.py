from model.SocailMediaDataModel import SocialMediaDataModel
import logging
import asyncio

log = logging.getLogger(__name__)

class WebScraperFacade:

    def __init__(self, query, max_results, socialMediaServices:list) -> None:
        self.query = query
        self.max_results = max_results
        self.services = socialMediaServices
        pass

    async def execute(self) -> SocialMediaDataModel:
        log.info('Social Media Analytics Facade has been called')
        result = SocialMediaDataModel()
        tasks = []
        for service in self.services:
            service_name = type(service).__name__
            log.info(f"Web Scraping Stated for App Name:{service_name}")
            tasks.append(service.getAnalytics(self.query, self.max_results))
        tasks_results = await asyncio.gather(*tasks)
        if tasks_results is not None:
            for i in tasks_results:
                result.users = result.users + i.users
        return result


        