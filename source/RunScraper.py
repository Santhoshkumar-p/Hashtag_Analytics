import logging
import sys

from controller.AnalyticsController import AnalyticsController

#Run Web Scraper And Analytics Services as sub process
#Web scraper will launch playwright which might interrupt streamlit browser interface
#that's why we are keeping it as separate subprocess

#SubProcess Log File Configuration
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
root_logger.propagate=False
root_logger.addHandler(console_handler)

log = logging.getLogger(__name__)

args = sys.argv[1:]
hashtag = args[0]
max_results = int(args[1])
controller = AnalyticsController(hashtag=hashtag, max_results=max_results)
data = controller.get_analytics_data()
if len(data) == 0:
    log.info(f'Web Scrapping and analytics is completed with error in subprrocess with size {len(data)}')
    sys.exit(1)
else: 
    log.info(f'Web Scrapping and analytics is completed in subprrocess with size {len(data)}')
    sys.exit(0)

