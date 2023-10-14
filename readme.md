<h1>Social Media Keyword Analytics Plaform</h1>

## How to setup the project?
Please install all the required libraries as specified in the requirements.txt file first
and choose the option of launching the app with or without GUI 

For pip users
```
pip install -r requirements.txt

```
For Anaconda environment users 

```
conda install --file requirements.txt

```

- Please do not be tempted to change the max crawling depth to 30, if you have patience to wait for the results, yes go ahead.
- As 'crawling depth' introduces multiple website launches, more data extraction and transformation that is inherently time consuming

## How to Launch the app with UI?

This App is utilizing streamlit library for UI components and charts. So to launch the app with UI
execute the following command after having installed all pip dependencies.

```
streamlit run ./source/AppDashboard.py
```

This will launch default browser window with homepage at http://localhost:8501/

## How to Launch the app wihtout UI?

#### Go to ./source/RunScraper.py (this is designed as a subprocess so comment out sys args) 

Just Replace this block
```
args = sys.argv[1:]
hashtag = args[0]
max_results = int(args[1])
controller = AnalyticsController(hashtag=hashtag, max_results=max_results)

```

with following block
```
#args = sys.argv[1:]
#hashtag = args[0]
#max_results = int(args[1])
controller = AnalyticsController(hashtag='Your Hashtag', max_results=5)

```

If you launch the app without UI, you will get to find the 
data files under the names(social_media_data.json -> Web Data, hashtag_analytics_data.json -> Analytics Data)

## Notes: 

Why have we setup subprocess?
 - streamlit or any webserver that launches UI will not allow any scraper to run out-of-the-box in the server's context. As scraping involved launching website and capturing data. This is considered as security threat to app servers. 
 - So we have decided to write scraper and UI as two different processes and allow them communicate over resource file
