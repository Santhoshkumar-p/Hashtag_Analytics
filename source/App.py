#Entry point for the app
import json
import os
import logging
from AppController import AppController
from SocailMediaDataModel import SocialMediaDataModel, SocialMediaDataModelEncoder

#APP NAME
APP_NAME = "SOCIAL_MEDIA_ANALYTICS"

#Log File Configuration
logging.basicConfig(
    filename='social_media_analytics.log',  # Specify the log file name
    filemode='w',
    level=logging.INFO,   # Set the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#Cosole Logs Configuration
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
root_logger = logging.getLogger()
root_logger.addHandler(console_handler)

#Current File Logger
log = logging.getLogger(__name__)

# Load environment variables from .env
def load_environment():
    with open('./source/.env') as env_file:
        for line in env_file:
            # Remove leading/trailing whitespace and split on '=' to separate key and value
            key, value = map(str.strip, line.strip().split('=', 1))

            # Set the environment variable
            os.environ[key] = value
        log.info("[1] Environment file has been loaded")

#Main Method
if __name__ == "__main__":
    load_environment()
    controller = AppController(query="ukraine", max_results=5)
    result = controller.getSocialMediaTrends()
    output_json = json.dumps(result, cls=SocialMediaDataModelEncoder, indent = 4)
    with open('./tiktok_analytics.json','w') as f:
        f.write(output_json)

