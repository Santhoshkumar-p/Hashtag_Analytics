from datetime import datetime
import json
import attr
from pandas import Timestamp

@attr.s(init=False)
class AnalyticsDataModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuickAnalytics) \
            or isinstance(obj, LatestMentions) \
            or isinstance(obj, TopInfluencers) \
            or isinstance(obj, RelatedHashTags):
            # Convert the SocialMediaDataModel object to a dictionary
            return obj.__dict__
        if isinstance(obj, Timestamp):
            return obj.timestamp()
        if isinstance(obj, datetime):
            return obj.timestamp()
        return super().default(obj)

@attr.s(init=False)
class QuickAnalytics:
    
    def __init__(self, mentions, interactions, reach, shares, likes):
        self.mentions = mentions
        self.interactions = interactions
        self.reach = reach
        self.shares = shares
        self.likes = likes
        pass

    def to_dict(self):
        return {
            "mentions": self.mentions,
            "interactions": self.interactions,
            "reach": self.reach,
            "shares": self.shares,
            "likes": self.likes,
        }

@attr.s(init=False)
class LatestMentions:

    def __init__(self, post, site, performance, date,post_link,no_of_likes,no_of_comments,no_of_views,sentiment, emoticon):
        self.post = post
        self.site = site
        self.performance = performance
        self.date = date
        self.post_link = post_link
        self.no_of_likes = no_of_likes
        self.no_of_comments = no_of_comments
        self.no_of_views = no_of_views
        self.sentiment = sentiment
        self.emoticon = emoticon

    def to_dict(self):
        return {
            "post": self.post,
            "site": self.site,
            "performance": self.performance,
            "date": self.date,
            "post_link": self.post_link,
            "no_of_likes": self.no_of_likes,
            "no_of_comments": self.no_of_comments,
            "no_of_views": self.no_of_views,
            "sentiment": self.sentiment,
            "emoticon":self.emoticon
        }

@attr.s(init=False)
class TopInfluencers:
    def __init__(self, user_id, user_name, avatar,no_of_followers,is_verified, no_of_mentions):
            self.user_id = user_id
            self.user_name = user_name
            self.avatar = avatar
            self.no_of_followers = no_of_followers
            self.is_verified = is_verified
            self.no_of_mentions = no_of_mentions

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "avatar": self.avatar,
            "no_of_followers": self.no_of_followers,
            "is_verified": self.is_verified,
            "no_of_mentions": self.no_of_mentions,
        }

@attr.s(init=False)
class RelatedHashTags:
    def __init__(self, hashtag, no_of_uses):
        self.hashtag = hashtag
        self.no_of_uses = no_of_uses
    
    def to_dict(self):
        return {
             "hashtag": self.hashtag,
             "no_of_uses": self.no_of_uses,
        }
    