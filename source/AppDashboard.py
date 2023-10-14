import asyncio
from itertools import groupby
import json
import logging
import os
import subprocess
import tempfile
import traceback
import streamlit as st
from controller.AnalyticsController import AnalyticsController
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="Hashtag Analytics",
    page_icon="👋",
    layout="centered",
)

if 'web_scraper_running' not in st.session_state \
        and 'IS_ENVIRONMENT_READY' not in st.session_state \
        and 'APP_STARTUP' not in st.session_state:
    st.session_state.web_scraper_running = False
    st.session_state.IS_ENVIRONMENT_READY = False
    st.session_state.APP_STARTUP = True


log = logging.getLogger(__name__)
#APP NAME
APP_NAME = "SOCIAL_MEDIA_ANALYTICS"

def read_analytics_data() -> dict:
    with open('hashtag_analytics_data.json', 'r') as f:
        data = json.load(f)
    return data

def file_analytics_data():
    with open('hashtag_analytics_data.json', 'r') as f:
        data = f.read()
    json_data = str(json.dumps(data))
    return json_data

@st.cache_data(show_spinner=False)    
def get_analytics_data(hashtag, max_results) -> dict:
    command = ["python", "./source/RunScraper.py", hashtag, str(max_results)]
    if st.session_state.APP_STARTUP is True:
        st.session_state.APP_STARTUP = False
        return read_analytics_data()
    if st.session_state.web_scraper_running is False :   
        log.info(f'********* Web Scraper Subprocess is running ********** {len(app.web_scraper_processes)}')  
        st.session_state.web_scraper_processes = True 
        st.session_state.APP_STARTUP = False
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            log.info(f'Web Scraping and analytics data extracted for hashtag {hashtag}')
            st.session_state.web_scraper_processes = False
            return read_analytics_data()
        else: 
            log.info(f'Some issue in analytics data extraction for hashtag {hashtag}')
            log.info(f'Returning historical data')
            return read_analytics_data()
    else: 
        return read_analytics_data()

#Header
def top_bar() -> str:
    h1,h2,h3 = st.columns([0.25, 0.75, 0.25])
    h1.write('Hashtag Analytics')
    with h2:
        hashtag = st.text_input(label="Keyword", label_visibility="collapsed", placeholder="Enter a hashtag", value='Nike')
    #center_column.button("Search")
    file_data = file_analytics_data()
    with h3:
        h3.download_button("Get Full Report",data=file_data,file_name='hashtag_analytics_report.json',mime='text/csv')
    return hashtag

#Side bar furture enhancements and max crawling depth 
def side_bar() -> int:
    max_results = st.sidebar.slider("Max Crawling Depth", min_value=0, max_value=30, value=5)
    log.info(f"Max Crawling Depth selected value {max_results}")
    return max_results
        

#Top Level Metrics Card
def metrics_bar(data) -> None:
    #Metrics Bar
    m2,m3,m4,m5,m6 = st.columns([0.20,0.20,0.20,0.20,0.20],gap='small')
    metrics = data['quick_analytics']
    m2.metric("Mentions", value=metrics['mentions'])
    m3.metric("Interactions", value=metrics['interactions'])
    m4.metric("Reach", value=metrics['reach'])
    m5.metric("Shares", value=metrics['shares'])
    m6.metric("Likes", value=metrics['likes'])

def latest_posts(data):
    st.write('Latest Mentions')
    latest_posts = [obj for obj in data['latest_mentions']]
    mentions_df = pd.DataFrame(latest_posts)
    mentions_df['date'] = pd.to_datetime(mentions_df['date'],unit='s')
    mentions_df = mentions_df.rename(columns={'post':'Post', 'site':'Site', 'performance':'Performance', 
                                'date':'Date', 'post_link':'Post Link', 'no_of_likes':'Likes',
                                'no_of_comments':'Comments','no_of_views':'Reach',
                                'emoticon':'Mood'})
    mentions_df = mentions_df.reindex(columns=['Post','Mood','Site','Date','Performance','Post Link','Likes','Comments','Reach'])
    st.data_editor(mentions_df, num_rows="fixed", hide_index=True, column_config={
        "Post Link": st.column_config.LinkColumn(
            "Post Link",
            help="The top trending social media apps",
            validate="^https://[a-z]+\.*\.com$",
            max_chars=200,
        )
    }, use_container_width=True,disabled=('Post','Site','Performance','Date','Post Link','Likes','Comments','Reach','Mood'))

def top_influencers(data) -> None:
    st.write('Top Influencers')
    top_influencers = [dict(obj) for obj in data['top_influencers']]
    influencers_df = pd.DataFrame(top_influencers)
    influencers_df = influencers_df.rename(columns={'user_id':'User Id',
                                                   'user_name':'User Name',
                                                   'avatar':'Avatar',
                                                   'no_of_followers':'No Of Followers',
                                                   'is_verified':'Verified',
                                                   'no_of_mentions':'Mentions'})
    influencers_df = influencers_df.reindex(columns=['Avatar','User Id','User Name','Verified','No Of Followers','Mentions'])
    st.data_editor(influencers_df, num_rows="fixed", hide_index=True, use_container_width=True, column_config={
                        "Avatar": st.column_config.ImageColumn("Avatar", help="Streamlit app preview screenshots")
                        },disabled=('User Id','User Name','Avatar','No Of Followers','Verified','Likes','Mentions'))

def related_hashtags(data) -> None:
    related_hashtags = data['related_hashtags']
    related_hashtags_df = pd.DataFrame(related_hashtags)
    if len(related_hashtags) > 0:
        related_hashtags_df = related_hashtags_df.rename(columns={'hashtag':'Hashtag','no_of_uses':'# of uses'})
    st.write('Related hashtags')
    st.data_editor(related_hashtags_df, num_rows="fixed", hide_index=True,use_container_width=True,disabled=('Hashtag','# of uses'))

#Latest Mentions
def recent_activities(data) -> None:
        r1,r2 = st.columns([0.6,0.4],gap='small')
        with r1.container():
            top_influencers(data)
        with r2.container():
            related_hashtags(data)

def reach_graph(data) -> None:
    st.write('Reach')
    st.write('No of views per day')
    views_per_day_df = pd.Series(data['views_per_day']).to_frame()
    views_per_day_df.index = pd.to_datetime(views_per_day_df.index)
    views_per_day_df_sorted = views_per_day_df.sort_index(ascending=True)
    st.line_chart(views_per_day_df_sorted)

def engagements_graph(data) -> None:
    st.write('Interactions')
    st.write('No of engagements per day')
    engagements_per_day_df = pd.Series(data['engagements_per_day']).to_frame()
    engagements_per_day_df.index = pd.to_datetime(engagements_per_day_df.index)
    engagements_per_day_df_sorted = engagements_per_day_df.sort_index(ascending=True)
    st.line_chart(engagements_per_day_df_sorted, color='#ffaa0088',use_container_width=True)

def mentions_by_weekday(data) -> None: 
    st.write('Mentions by Weekday')
    st.write('Weekday Keyword Highlights')
    mentions_by_weekday_df = pd.Series(data['mentions_by_weekday']).to_frame()
    st.bar_chart(mentions_by_weekday_df, color='#fa6c8d')

#Analytics
def metrics_analytics(data) -> None:
    a1, a2, a3 = st.columns(3)
    with a1.container():
        reach_graph(data)
    with a2.container():
        engagements_graph(data)
    with a3.container():
        mentions_by_weekday(data)

def trends_graph(data) -> None:
    st.write('Google Search Trends')
    st.write('Searches/Month')
    trends_df = pd.DataFrame(pd.read_json(json.dumps(data['trends_overtime'])))
    trends_df = trends_df.drop(columns='isPartial')
    trends_df = trends_df.set_index('date')
    st.line_chart(trends_df, color='#8BC34A')

def sentiment_analysis(data) -> None:
    sentiment = st.container()
    sentiment.write('Sentiment Analysis')
    sentiment.write('Sentiment Score Over Time')
    sentiments_df_raw = pd.DataFrame(data['sentiments_over_time'])
    #sentiments_df =  sentiments_df.iloc[0].astype('datetime64[as]')
    sentiments_df = pd.DataFrame()
    sentiments_df['date'] = sentiments_df_raw.iloc[:, 0:1]
    sentiments_df['sentiment_score'] = sentiments_df_raw.iloc[:, 1:2]
    sentiments_df = sentiments_df.set_index('date')
    sentiments_df.index = pd.to_datetime(sentiments_df.index, unit='s')
    sentiment.bar_chart(sentiments_df, color="sentiment_score")


def geo_analytics(data) -> None:
    #WorldMap
    heatmap = st.container()
    if data['interest_by_region']:
        heatmap.write('Trending all over the world')
        countries = next(iter(data["interest_by_region"].values()))
        region_df = pd.Series(countries).to_frame()
        min_value = region_df[0].min()
        max_value = region_df[0].max()
        fig = px.choropleth(locations=region_df.index, locationmode="country names", 
                                color=region_df[0],color_continuous_scale="sunset",
                                range_color=[min_value, max_value],title="Hashtag Mentions Distribution - Worldwide")
        fig.update_geos(fitbounds="locations", visible=True)
        st.plotly_chart(fig)
 

def source_plot(data) -> None:
    sources = st.container()
    sources.write('Sources')
    results = {}
    for post in data['latest_mentions']:
        if post['site'] in results:
            results[post['site']]+= 1
        else:
           results[post['site']] = 1
    sources_df = pd.DataFrame({'Platform': list(results.keys()),
                                'Count': list(results.values())})
    fig = px.pie(sources_df, values='Count', names='Platform',
                 title=f'Distribution of Sources',
                 height=300, width=200, color='Count')
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)

# def language_plot() -> None:
#     st.write('Languages')
#     sources = st.selectbox('Language', ['english', 'spanish', 'french'])
#     platform_data = {
#     'languages': ['english', 'spanish', 'french'],
#     'english': [12, 1, 20,],
#     'spanish': [4,4, 12],
#     'french': [24, 7, 62]}
#     fig = px.pie(platform_data, values=sources, names='languages',
#                  title=f'number of {sources} mentions',
#                  height=300, width=200)
#     fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
#     st.plotly_chart(fig, use_container_width=True)

#RelatedAnalytics
# def related_analytics() -> None:
#     a1, a2, a3 = st.columns(3)
#     with a1.container():
#         source_plot()
#     with a2.container():
#         language_plot()
#     with a3.container():
#         mentions_by_weekday()


def launch_dashboard() -> None:
    keyword = top_bar()
    max_results = side_bar()
    #Run web scraper and analytics engine
    with st.spinner('Hang on tight 🤞'):
        data = get_analytics_data(keyword, max_results)
    st.success('Done!')
    ui_elements = [metrics_bar, latest_posts, recent_activities, metrics_analytics, geo_analytics, trends_graph, sentiment_analysis, source_plot]
    # analytics, geo_analytics, related_analytics
    for ui in ui_elements:
        ui(data)
    st.write('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    st.write("                   Made with ❤️ in Data Focused Python Class Project                  ")

def setup_log_environment() -> bool:
    #Log File Configuration
    logging.basicConfig(
        filename='app_dashboard.log',  # Specify the log file name
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
    if len(root_logger.handlers) <= 1:
        root_logger.addHandler(console_handler)
        return True
    return True










#Entry Point to the app
#Use command -> streamlit run /{absolute path}/LaunchApp.py
try:
    if st.session_state.IS_ENVIRONMENT_READY is False:
        setup_log_environment()
    launch_dashboard()
except:
    log.info("Exception in dashboard")
    log.error(f'{traceback.print_exc()}')


