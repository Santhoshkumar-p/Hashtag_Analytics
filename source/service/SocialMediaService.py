import logging
import os
import re
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import requests
from model.SocailMediaDataModel import Location, SocialMediaDataModel

log = logging.getLogger(__name__)

class SocialMediaService:

    GEO_LOCATION_URL = "https://api.geoapify.com/v1/geocode/search?format=json&"

    async def getAnalytics(self, hashtag, max_results) -> SocialMediaDataModel:
        pass

    async def extract_geo_location(self, desc) -> Location: 
        geo_location_api_key = os.environ.get('GEO_API_KEY')
        log.info("Geo Location API Secret Key Retrieved")
        url_params = {'text': {desc}, 'apiKey': {geo_location_api_key}}
        parsed_url = urlparse(self.GEO_LOCATION_URL)

        query_params = parse_qs(parsed_url.query)

        # Add or modify query parameters
        query_params["text"] = [{desc}]
        query_params["apiKey"] = [{geo_location_api_key}]

        updated_query_string = urlencode(query_params, doseq=True)
        new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, updated_query_string, parsed_url.fragment))

        log.info(f"Geo Location API URL {new_url}")
        
        with requests.get(new_url) as response: 
            response_json = response.json()
            
            if 'results' in response_json and response_json['results']:
                location = Location(**response_json['results'][0])
                log.info("`GeoLocation data found in the API response")
                return location
            else: 
                log.info("No Geolocation data found in the API response")
                return None
    
    def extract_location(self, desc) -> str:
        location_pattern = r"in ([\w\s]+), ([\w\s]+)"
        match = re.search(location_pattern, desc)
        location = None
        if match:
            city = match.group(1)
            state = match.group(2)
            location = f"{city}, {state}"
            log.info(f"Location found in the desc:{location}")
            return location
        else:
            log.info("Location not found in the input string.")
            return location