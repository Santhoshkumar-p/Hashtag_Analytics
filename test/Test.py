import requests
import re
import logging

log = logging.getLogger(__name__)
url = "https://api.geoapify.com/v1/geocode/search?text=Greenville%2C%20South%20Carolina&format=json&apiKey=1b48259b810e48ddb151889f9ea58db0"
          
response = requests.get(url)
print(response.json())


def extract_location(desc) -> str:
        location_pattern = r"in ([\w\s]+), ([\w\s]+)"
        match = re.search(location_pattern, desc)
        location = None
        if match:
            city = match.group(1)
            state = match.group(2)
            location = f"{city}, {state}"
            log.info("Location:", location)
            return location
        else:
            log.info("Location not found in the input string.")
            return location
