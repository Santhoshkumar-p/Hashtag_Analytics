import logging
from model.AnalyticsModel import LatestMentions, QuickAnalytics, RelatedHashTags, TopInfluencers
from model.SocailMediaDataModel import SocialMediaDataModel
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import operator
import pandas as pd
import numpy as np
import datetime as datetime
from pytrends.request import TrendReq
import warnings

nltk.downloader.download('vader_lexicon')
# Suppress all FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)
log = logging.getLogger(__name__)

class AnalyticsService:

    def __init__(self) -> None:
        pass

    def format_number(self, number):
        # List of suffixes for thousands, millions, billions, etc.
        suffixes = ["", "K", "M", "B", "T"]
        # Determine the appropriate suffix and format the number
        suffix_index = 0
        while abs(number) >= 1000 and suffix_index < len(suffixes) - 1:
            number /= 1000.0
            suffix_index += 1
        # Format the number with the appropriate suffix
        number = f"{number:.1f}{suffixes[suffix_index]}"
        return number
        
    
    def perform_sentiment_analysis(self, text:str, score_needed=False) -> str:
        
        sia = SentimentIntensityAnalyzer()
        
        sentiment_scores = sia.polarity_scores(text)
        compound_score = sentiment_scores['compound']

        if(score_needed):
            return compound_score
        else:
            if compound_score >= 0.05:
                sentiment = 'positive'
            elif compound_score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            return sentiment
        
    def get_sentiment_emojis(self, data) -> str:
        if data == 'negative':
            return '😬'
        elif data == 'positive':
            return '😃'
        else:
            return '😑'
    
    
   
    def calculate_quick_analytics(self, socMediaData:SocialMediaDataModel) -> QuickAnalytics:
        mentions = self.format_number(sum(post.no_of_mentions for user in socMediaData.users for user_model in user for post in user_model.posts))
        interactions = self.format_number(sum(post.no_of_comments for user in socMediaData.users for user_model in user for post in user_model.posts))
        reach = self.format_number(sum(post.no_of_views for user in socMediaData.users for user_model in user for post in user_model.posts))
        shares = self.format_number(sum(post.no_of_shares for user in socMediaData.users for user_model in user for post in user_model.posts))
        likes = self.format_number(sum(post.no_of_likes for user in socMediaData.users for user_model in user for post in user_model.posts))
        return QuickAnalytics(mentions=mentions, interactions=interactions, likes=likes, reach=reach, shares=shares)

    def aggregate_latest_mentions(self, socMediaData:SocialMediaDataModel) -> list:
        latest_mentions = []

        for socMedUser in socMediaData.users:
            for user in socMedUser:
                site = user.platform
                for post in user.posts:
                    performance = post.performance
                    date = post.post_date
                    post_link = post.post_link
                    no_of_likes = self.format_number(post.no_of_likes)
                    no_of_comments = self.format_number(post.no_of_comments)
                    no_of_views = self.format_number(post.no_of_views)
                    text = post.caption
                    sentiment = self.perform_sentiment_analysis(text,False)
                    emoticon = self.get_sentiment_emojis(sentiment)
                    post = post.caption
                    latest_mention = LatestMentions(post,site,performance,date,post_link,no_of_likes,no_of_comments,no_of_views,sentiment,emoticon)
                    latest_mentions.append(latest_mention)
        return latest_mentions
                    
    def get_top_influencers(self, socMediaData:SocialMediaDataModel) -> list:      
        top_influencers = []
        for socMedUser in socMediaData.users:
                for user in socMedUser:
                    user_id = user.user_id
                    user_name = user.nickname
                    avatar = user.avatar_link
                    no_of_followers = user.follower_count
                    is_verified = user.verified
                    no_of_mentions = user.impressions
                    top_influencer = TopInfluencers(user_id, user_name, avatar, no_of_followers, is_verified, no_of_mentions)
                    top_influencers.append(top_influencer)
        return top_influencers



        
    def related_hashatags(self,socMediaData:SocialMediaDataModel) -> list:
        related_hashtags = []
        all_hashtags = [post.hashtags for user in socMediaData.users for user_model in user for post in user_model.posts]
        hashtags = [tag for sublist in all_hashtags for tag in sublist]
        hashtag_counts = {}
        # Count the occurrences of each hashtag
        for hashtag in hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += 1
            else:
                hashtag_counts[hashtag] = 1
        # Convert the dictionary to a list of tuples (hashtag, count)
        related_hashtags = [RelatedHashTags(hashtag, count) for hashtag, count in hashtag_counts.items()]
        return related_hashtags
    
    def get_views_per_day(self, socMediaData:SocialMediaDataModel) -> dict:
        views_per_day = dict()
        
        views_by_date = [(datetime.datetime.fromtimestamp(float(post.post_date)),post.no_of_views) for user in socMediaData.users for user_model in user for post in user_model.posts]
        for elem in views_by_date:
            date_obj = elem[0].strftime("%m-%d-%Y")
            if date_obj in views_per_day:
                views_per_day[date_obj] += elem[1]
            else: 
                views_per_day[date_obj] = elem[1]
        
        return views_per_day

    def get_engagements_per_day(self, socMediaData:SocialMediaDataModel) -> dict:
        engagements_per_day = dict()
        
        engagement_by_date = [(datetime.datetime.fromtimestamp(float(post.post_date)), post.no_of_comments) for user in socMediaData.users for user_model in user for post in user_model.posts]
        for elem in engagement_by_date:
            date_obj = elem[0].strftime("%m-%d-%Y")
            if date_obj in engagements_per_day:
                engagements_per_day[date_obj] += elem[1]
            else: 
                engagements_per_day[date_obj] = elem[1]
        
        return engagements_per_day
    
    def get_mentions_by_weekday(self, socMediaData:SocialMediaDataModel) -> dict:
        mentions_by_weekday = dict()
        
        mentions_by_day = [(datetime.datetime.fromtimestamp(float(post.post_date)), post.no_of_mentions) for user in socMediaData.users for user_model in user for post in user_model.posts]
        for elem in mentions_by_day:
            date_obj = elem[0].strftime("%A")
            if date_obj in mentions_by_weekday:
                mentions_by_weekday[date_obj] += elem[1]
            else: 
                mentions_by_weekday[date_obj] = elem[1]
        
        return mentions_by_weekday
    
    def get_sentiments_over_time(self, socMediaData:SocialMediaDataModel) -> list:
        sentiments_over_time = list()
        sentiments_over_time = [(float(post.post_date), self.perform_sentiment_analysis(post.caption,score_needed=True)) for user in socMediaData.users for user_model in user for post in user_model.posts]
        return sentiments_over_time

    def get_trends_analysis(self, keyword) -> dict:
        trends_dict = dict()
        pytrends = TrendReq(hl='en-US', tz=360)
        kw_list = [keyword] 
        pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m') 
        try:
            data = pytrends.interest_over_time() 
            data = data.reset_index() 
            data['date'].astype(str)
            trends_dict['interest_over_time'] = data.to_dict()
        except Exception as e:
            log.info('Exception occured from Trends API getting interest over time response')
            log.error(e.with_traceback)
            trends_dict['interest_over_time'] = None
        # import plotly.express as px
        # fig = px.line(data, x="date", y=['machine learning'], title='Keyword Web Search Interest Over Time')
        # fig.show() 
        try:
            by_region = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
            trends_dict['interest_by_region'] = by_region.to_dict()
        except Exception as e:
            log.info('Exception occured from Trends API from getting interest by region response')
            trends_dict['interest_by_region'] = None
            log.error(e.with_traceback)
        return trends_dict
            
        
    def run_analytics(self, socialMediaData,keyword=None) -> dict:
        analytics = dict()
        
        analytics['quick_analytics'] = self.calculate_quick_analytics(socialMediaData).to_dict()
        analytics['latest_mentions'] = list((x.to_dict()) for x in self.aggregate_latest_mentions(socialMediaData))
        analytics['top_influencers'] = list((x.to_dict()) for x in self.get_top_influencers(socialMediaData))
        analytics['related_hashtags'] = list((x.to_dict()) for x in self.related_hashatags(socialMediaData))
        analytics['views_per_day'] = self.get_views_per_day(socialMediaData)
        analytics['engagements_per_day'] = self.get_engagements_per_day(socialMediaData)
        analytics['mentions_by_weekday'] = self.get_mentions_by_weekday(socialMediaData)
        analytics['sentiments_over_time'] = list((float(x[0]), x[1]) for x in self.get_sentiments_over_time(socialMediaData))
        if keyword != None:
            trends_analysis = self.get_trends_analysis(keyword)
            analytics['trends_overtime'] = trends_analysis['interest_over_time']
            analytics['interest_by_region'] = trends_analysis['interest_by_region']

        return analytics