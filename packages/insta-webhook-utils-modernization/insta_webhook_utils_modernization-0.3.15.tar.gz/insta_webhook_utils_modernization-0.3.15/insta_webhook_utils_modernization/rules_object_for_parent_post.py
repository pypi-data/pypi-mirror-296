import html
import re
from datetime import datetime

from insta_webhook_utils_modernization.common_functions import get_media_type
from insta_webhook_utils_modernization.indentifier_code import InstaChannelsEnum, InstaPostChannelType, MentionPostType, \
    TypeOfComment


def check_is_brand_mention(value, **kwargs):
    is_brand_post = kwargs.get('data', {}).get("is_brand_post", False)
    if is_brand_post:
        return True
    return False


def check_type_of_comment_handler(value, **kwargs):
    return TypeOfComment.ActualPost.value


def url_handler(value, **kwargs):
    screen_name = kwargs.get("data").get("comment_username")
    if not screen_name:
        screen_name = kwargs.get("data").get("username")
    url = f"https://www.instagram.com/{screen_name}/"
    return url


def handle_insta_post_type(value, **kwargs):
    is_brand_post = kwargs.get('data', {}).get("is_brand_post", False)
    is_stories = kwargs.get('data', {}).get("is_for_stories", False)
    is_mention_post = kwargs.get('data', {}).get("is_mention_post", False)
    is_stories_mention = kwargs.get('data', {}).get("is_stories_mention", False)
    if is_stories and is_brand_post and is_stories is not None:
        return InstaPostChannelType.STORIES.value
    if is_brand_post and is_brand_post is not None:
        return InstaPostChannelType.BRAND.value
    if is_mention_post and is_mention_post is not None:
        return InstaPostChannelType.MENTION.value
    if is_stories_mention and is_stories_mention is not None:
        return InstaPostChannelType.STORIES_MENTION.value


def get_hashtags(text, **kwargs):
    if not text:
        return ""
    # Regular expression to match hashtags
    regex = r'(?<=#)\w+'
    # Find all matches of the regex
    hashtags = re.findall(regex, text)
    # Join the matches with a comma
    return hashtags


def handle_media_type(value, **kwargs):
    return get_media_type(value)


def parent_chanel_handler(value, **kwargs):
    return InstaChannelsEnum.InstagramPagePosts.value


def escape_url(url):
    # Escape special characters in the URL
    return html.escape(url)


def parent_post_time_handler(value, **kwargs):
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
    return dt.strftime('%Y-%m-%dT%H:%M:%S')


def utc_time_to_iso_format(current_time=None, **kwargs):
    return datetime.utcnow().isoformat()


def parent_post_description_handler(value, **kwargs):
    if value:
        return value.replace("\n", " ").replace("\r", " ")
    return ""


def parent_post_is_brand_post_handler(setting_author_id, **kwargs):
    is_brand_post = kwargs.get("data", {}).get("is_brand_post", None)
    if is_brand_post is not None:
        return is_brand_post
    if int(setting_author_id) == int(kwargs['data'].get('owner', {}).get('id', 0)):
        return True
    return False


def post_type_handler(setting_author_id, **kwargs):
    is_brand_post = kwargs.get("data", {}).get("is_brand_post", None)
    if is_brand_post and is_brand_post is not None:
        return MentionPostType.BrandPost.value
    if int(setting_author_id) == int(kwargs['data'].get('owner', {}).get('id', 0)):
        return MentionPostType.BrandPost.value
    return MentionPostType.UserPost.value


rules_obj = {
    "RawData.SettingID": {
        "keys": ["setting_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "settingid",
        "mandatory": True,
        "skip_if_missing": False
    },
    "isBrandPost": {
        "keys": ["author_social_id"],
        "default_value": 0,
        "handler_function": parent_post_is_brand_post_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.PageName": {
        "keys": ["setting_id"], 
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "m_pagename",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.InstagramPostType": {
        "keys": ["instagram_post_type_data"],
        "default_value": None,
        "handler_function": handle_insta_post_type,
        "clickhouse_column_name": "instagram_post_type",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.DataCollection": {
        "keys": [],
        "default_value": 1,
        "handler_function": None,
        "clickhouse_column_name": "data_collection",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.CreatedDate": {
        "keys": ["timestamp"],
        "default_value": datetime.utcnow,
        "handler_function": parent_post_time_handler,
        "clickhouse_column_name": "created_date",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Url": {
        "keys": ["permalink"],
        "default_value": "",
        "handler_function": None,
        "clickhouse_column_name": "url",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.InstagramGraphApiID": {
        "keys": ["post_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "InstagramGraphApiID",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.SocialID": {
        "keys": ["post_id"],
        "default_value": None,
        "handler_function": None,
        "clickhouse_column_name": "tweetidorfbid",
        "mandatory": True,
        "skip_if_missing": False
    },

    "RawData.IsDarkPost": {
        "keys": ["is_dark_post"],
        "default_value": False,
        "handler_function": None,
        "clickhouse_column_name": "isdarkpost",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Typeofcomment": {
        "keys": ["type_of_comment"],
        "default_value": False,
        "handler_function": check_type_of_comment_handler,
        "clickhouse_column_name": "isdarkpost",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.IsBrandMention": {
        "keys": [""],
        "default_value": False,
        "handler_function": check_is_brand_mention,
        "clickhouse_column_name": "isbrandmention",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.Description": {
        "keys": ["caption"],
        "default_value": "",
        "handler_function": parent_post_description_handler,
        "clickhouse_column_name": "description",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.LanguageName": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.Lang": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.Hastagcloud": {
        "keys": ["caption"],
        "default_value": [],
        "handler_function": get_hashtags,
        "clickhouse_column_name": "Hastagcloud",
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.CountryCode": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.NumCommentsCount": {
        "keys": ["comments_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.NumLikesCount": {
        "keys": ["like_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.PostInsights": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True

    },
    "RawData.NumLikesORFollowers": {
        "keys": ["owner.followers_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.NumVideoViews": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.NumShareCount": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.DurationInSeconds": {
        "keys": [],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.ShareURL": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "clickhouse_column_name": "m_share_url",
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.PostPermissions": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.SimplifiedText": {
        "keys": ["caption"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.PostType": {
        "keys": ["author_social_id"],
        "default_value": 0,
        "handler_function": post_type_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.VideoDetails": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.MusicDetails": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True

    },
    "RawData.AttachmentXML": {
        "keys": ["attachment_xml"],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": False
    },
    "RawData.MediaType": {
        "keys": ["media_type"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False

    },
    "RawData.MediaEnum": {
        "keys": ["media_type"],
        "default_value": "",
        "handler_function": handle_media_type,
        "mandatory": True,
        "skip_if_missing": False

    },
    "ChannelGroup": {
        "keys": ["channel_group_id"],
        "default_value": 3,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "ChannelType": {
        "keys": ["channel_type"],
        "default_value": "",
        "handler_function": parent_chanel_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandID": {
        "keys": ["brand_id"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandName": {
        "keys": ["brand_name"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.CategoryID": {
        "keys": ["category_id"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.CategoryName": {
        "keys": ["category_name"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.BrandSettings": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "BrandInfo.OperationEnum": {
        "keys": [],
        "default_value": None,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "ServiceName": {
        "keys": [],
        "default_value": "instagram_utils_parent_modernization",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "MentionTrackingDetails.FetchingServiceInTime": {
        "keys": ["in_time"],
        "default_value": datetime.utcnow().isoformat(),
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "MentionTrackingDetails.FetchingServiceOutTime": {
        "keys": [],
        "default_value": "",
        "handler_function": utc_time_to_iso_format,
        "mandatory": True,
        "skip_if_missing": False
    },
    # User Model Rules Start Here
    "RawData.UserInfo.ScreenName": {
        "keys": ["username"],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorName": {
        "keys": ["username"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.ScreenNameModifiedDate": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Gender": {
        "keys": [],
        "default_value": -1,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.PicUrl": {
        "keys": ["owner.profile_picture_url"],
        "default_value": "",
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.Url": {
        "keys": ["owner"],
        "default_value": "",
        "handler_function": url_handler,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.UpdatedDate": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsVerified": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.LanguageJson": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.AuthorSocialID": {
        "keys": ["owner.id", "post_author_id"],
        "default_value": False,
        "handler_function": None,
        "mandatory": True,
        "skip_if_missing": False
    },
    "RawData.UserInfo.IsMuted": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.FollowingCount": {
        "keys": ["owner.follows_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.FollowersCount": {
        "keys": ["owner.followers_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Insights": {
        "keys": [],
        "default_value": {},
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.TweetCount": {
        "keys": ["owner.media_count"],
        "default_value": 0,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsBlocked": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsHidden": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.IsUserPrivate": {
        "keys": [],
        "default_value": False,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.SocialChannels": {
        "keys": [],
        "default_value": [],
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.ChannelGroupID": {
        "keys": ["channel_group_id"],
        "default_value": None,
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.country": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.country_code": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    },
    "RawData.UserInfo.Location.locationname": {
        "keys": [],
        "default_value": "",
        "handler_function": None,
        "mandatory": False,
        "skip_if_missing": True
    }
}
