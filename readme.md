<h1>Social Media Keyword Analytics Plaform</h1>

## What is it?

Demo Video Link -> (https://clipchamp.com/watch/mXZhUSxp1NY)

[<img src="https://github.com/Santhoshkumar-p/Hashtag_Analytics/assets/24734488/93b05353-65d3-4e75-a02e-7ed55089c75f" width="50%">]
![localhost_8501_ (5)](https://github.com/Santhoshkumar-p/Hashtag_Analytics/assets/24734488/721708be-0972-48be-8b7f-172c014b3d4a)
![localhost_8501_ (7)](https://github.com/Santhoshkumar-p/Hashtag_Analytics/assets/24734488/1043b355-462e-4785-a85d-8e55bbce64dc)
![localhost_8501_](https://github.com/Santhoshkumar-p/Hashtag_Analytics/assets/24734488/231da13b-d8e1-400c-a1cc-80928e6262c1)


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

Just Execute the below python command in CLI
```
python your_directory\source\RunScraper.py 'nike' '5'

or

python your_directory\source\RunScraper.py 'nike' 5
```
here 'nike' is the hashtag
      5 is the max crawling depth

If you launch the app without UI, you will get to find the 
data files under the names(social_media_data.json -> Web Data, hashtag_analytics_data.json -> Analytics Data)

## Notes: 

Why have we setup subprocess?
 - streamlit or any webserver that launches UI will not allow any scraper to run out-of-the-box in the server's context. As scraping involved launching website and capturing data. This is considered as security threat to app servers. 
 - So we have decided to write scraper and UI as two different processes and allow them communicate over resource file
