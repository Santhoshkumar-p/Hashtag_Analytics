
import json

class SocialMediaDataModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, SocialMediaDataModel) \
            or isinstance(obj, SocialMediaUserModel) \
            or isinstance(obj, SocialMediaPostModel) \
            or isinstance(obj, Location):
            # Convert the SocialMediaDataModel object to a dictionary
            return obj.__dict__
        return super().default(obj)

class SocialMediaDataModel:
    def __init__(self, users=list()) -> None:
        self.users = [[SocialMediaUserModel(**user) for user in users]]
        pass
    
    def get_no_of_users(self) -> int:
        return len(self.users)

class SocialMediaPostModel:
    def __init__(self, caption, post_id, post_link, no_of_likes, no_of_comments, no_of_shares, no_of_views,
                 post_date, language, hashtags, location=None, extra_stats=None):
        self.caption = caption
        self.post_id = post_id
        self.post_link = post_link
        self.no_of_likes = no_of_likes
        self.no_of_comments = no_of_comments
        self.no_of_shares = no_of_shares
        self.no_of_views = no_of_views
        self.post_date = post_date
        self.location = location
        self.language = language
        self.hashtags = hashtags
        self.extra_stats = extra_stats or {}

    def __str__(self):
        return f"Caption: {self.caption}, Likes: {self.no_of_likes}, Comments: {self.no_of_comments}"

class SocialMediaUserModel:
    def __init__(self, user_id, nickname, user_bio, is_user_private, follower_count, following_count,
                 total_posts,impressions, avatar_link, verified, platform, posts):
        self.user_id = user_id
        self.nickname = nickname
        self.user_bio = user_bio
        self.is_user_private = is_user_private
        self.follower_count = follower_count
        self.following_count = following_count
        self.total_posts = total_posts
        self.impressions = impressions
        self.avatar_link = avatar_link
        self.verified = verified
        self.platform = platform
        self.posts = [SocialMediaPostModel(**post_data) for post_data in posts]

    def __str__(self):
        return f"User ID: {self.user_id}, Nickname: {self.nickname}, Follower Count: {self.follower_count}"

class Location:
    def __init__(self, country, country_code, state, county, city, lon, lat, state_code, formatted):
        self.country = country
        self.country_code = country_code
        self.state = state
        self.county = county
        self.city = city
        self.lon = lon
        self.lat = lat
        self.state_code = state_code
        self.formatted = formatted
        

    def __str__(self):
        return f"{self.city}, {self.state}, {self.country}"
    

