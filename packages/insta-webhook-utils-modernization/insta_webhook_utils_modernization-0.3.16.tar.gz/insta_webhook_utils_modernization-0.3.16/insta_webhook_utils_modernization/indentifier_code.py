import json
import traceback
from enum import Enum
from typing import Dict, Any, Optional, List


class TypeOfComment(Enum):
    UserParentPost = 0  # Parent post is User
    BrandParentPost = 1  # Parent post is Brand
    ActualPost = 2  # Actual Post

    @classmethod
    def get_name_by_value(cls, value):
        """Helper method to get the enum name by its value."""
        for comment_type in cls:
            if comment_type.value == value:
                return comment_type.name
        return None  # Return None if no match found

    @classmethod
    def get_value_by_name(cls, name):
        """Helper method to get the enum value by its name."""
        try:
            return cls[name].value
        except KeyError:
            return None  # Return None if the name does not exist


class MentionPostType(Enum):
    BrandPost = 1
    UserPost = 2
    BrandComment = 3
    UserComment = 4
    NonSocialChannel = 5
    UserPrivateMessages = 6
    BrandPrivateMessages = 7
    UserShare = 8
    BrandShare = 9
    TwitterBrandReply = 10
    TwitterUserReply = 11
    PublicPosts = 12
    BrandReview = 13
    UserReviews = 14
    Other = 15

    @classmethod
    def get_name_by_value(cls, value):
        """Helper method to get the enum name by its value."""
        for post_type in cls:
            if post_type.value == value:
                return post_type.name
        return None  # Return None if no match found

    @classmethod
    def get_value_by_name(cls, name):
        """Helper method to get the enum value by its name."""
        try:
            return cls[name].value
        except KeyError:
            return None  # Return None if the name does not exist


# Enum for Channels
class ChannelEnum(Enum):
    DM = "14"
    REPLY_STORY = "28"
    POST = "15"
    COMMENT = "29"
    MENTION = "16"


# Enum for Topics
class TopicEnum(Enum):
    DM_STANDBY = "InstaWebhookDmStandByTopic"
    STORY_TOPIC = "InstaWebhookStoryTopic"
    POST_TOPIC = "InstaWebhookPostTopic"
    COMMENTS_TOPIC = "InstaWebhookCommentsTopic"


class InstaChannelsEnum(Enum):
    InstagramPagePosts = 20
    InstagramUserPosts = 21
    InstagramComments = 22
    InstagramPublicPosts = 23
    InstagramMessages = 70


class InstaPostChannelType(Enum):
    BRAND = 1
    MENTION = 2
    PUBLIC = 3
    STORIES = 4
    DUMMY_POST = 5
    TAGS = 6
    IGTV = 7
    REELS = 8
    ADS = 9
    REVIEWS = 10
    STORIES_MENTION = 11
    RECOMMENDATION = 12


class InstagramEventType(Enum):
    MESSAGE = ("message", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STORY_INSIGHTS = ("story_insights", "", "")
    MESSAGE_WITH_VIDEO = ("message_with_video", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    COMMENT_ON_REEL = ("comment_on_reel", ChannelEnum.COMMENT, TopicEnum.COMMENTS_TOPIC)
    COMMENT_ON_FEED = ("comment_on_feed", ChannelEnum.COMMENT, TopicEnum.COMMENTS_TOPIC)
    COMMENT_REPLY_ON_FEED = ("comment_reply_on_feed", ChannelEnum.COMMENT, TopicEnum.COMMENTS_TOPIC)
    COMMENT_ON_AD = ("comment_on_ad", ChannelEnum.COMMENT, TopicEnum.COMMENTS_TOPIC)
    MENTION_IN_COMMENT = ("mention_in_comment", ChannelEnum.MENTION, TopicEnum.COMMENTS_TOPIC)
    STORY_MENTION = ("story_mention", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    UNSUPPORTED_ATTACHMENT = ("unsupported_attachment", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    MENTION_IN_FEED = ("mention_in_feed", ChannelEnum.POST, TopicEnum.POST_TOPIC)
    STANDBY_READ = ("standby_read", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_REPLY_TO_MESSAGE = ("standby_reply_to_message", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_SIMPLE_MESSAGE = ("standby_simple_message", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    PASS_THREAD_CONTROL = ("pass_thread_control", "", "")
    STANDBY_TAKE_THREAD_CONTROL = ("standby_take_thread_control", "", "")
    MENTION_IN_MEDIA = ("mention_in_media", ChannelEnum.POST, TopicEnum.POST_TOPIC)
    MESSAGE_REACT = ("message_react", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    MESSAGE_UNREACT = ("message_unreact", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_IMAGE = ("standby_message_with_image", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_VIDEO = ("standby_message_with_video", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_UNSUPPORTED_ATTACHMENT = (
        "standby_message_with_unsupported_attachment", "", "")
    STANDBY_REACTION = ("standby_reaction", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_SHARE = ("standby_message_with_share", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_REEL = ("standby_message_with_reel", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_STORY_MENTION = ("standby_story_mention", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_DELETED = ("standby_message_deleted", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    STANDBY_MESSAGE_WITH_AUDIO = ("standby_message_with_audio", ChannelEnum.DM, TopicEnum.DM_STANDBY)
    POSTBACK = ("postback", "", "")
    REQUEST_THREAD_CONTROL = ("request_thread_control", "", "")
    REPLY_TO_STORY = ("reply_to_story", ChannelEnum.REPLY_STORY, TopicEnum.DM_STANDBY)
    STANDBY_UNSUPPORTED = ("standby_unsupported", "", "")
    MESSAGE_TEMPLATE = ("message_template", "", "")
    MESSAGE_READ = ("message_read", "", "")
    MESSAGE_DELETED = ("message_deleted", "", "")

    def __init__(self, event_type, channel, topic):
        self._event_type = event_type
        self._channel = channel
        self._topic = topic

    @property
    def event_type(self):
        return self._event_type

    @property
    def channel(self):
        return self._channel if self._channel else "N/A"

    @property
    def topic(self):
        return self._topic if self._topic else "N/A"

    @classmethod
    def get_events_by_channel(cls, channel):
        """
        Get all events that match a specific channel.
        """
        return [event for event in cls if event.channel == channel]

    @classmethod
    def get_events_by_topic(cls, topic):
        """
        Get all events that match a specific topic.
        """
        return [event for event in cls if event.topic == topic]

    @classmethod
    def get_missing_channels(cls):
        """
        Get all events that are missing channel mappings.
        """
        return [event for event in cls if event.channel == "N/A"]

    @classmethod
    def get_missing_topics(cls):
        """
        Get all events that are missing topic mappings.
        """
        return [event for event in cls if event.topic == "N/A"]

    @classmethod
    def list_all_events(cls):
        """
        List all event types available in the enum.
        """
        return [event.event_type for event in cls]

    def __str__(self):
        return f"EventType: {self.event_type}, Channel: {self.channel}, Topic: {self.topic}"


def process_media_event(changes_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process media-related events like comments or mentions using a mapping approach."""

    media_type = changes_value.get('media', {}).get('media_product_type')

    # Mapping media types to InstagramEventType
    media_type_mapping = {
        'REELS': InstagramEventType.COMMENT_ON_REEL,
        'FEED': InstagramEventType.COMMENT_ON_FEED,
        'AD': InstagramEventType.COMMENT_ON_AD
    }

    # Check if media_type exists in the mapping
    if media_type == 'FEED' and 'parent_id' in changes_value:
        return InstagramEventType.COMMENT_REPLY_ON_FEED

    return media_type_mapping.get(media_type.upper() if media_type else None)


def process_mentions_event(changes_value: Dict[str, Any], changes_field: str) -> Optional[InstagramEventType]:
    """Process mention-related events."""
    if changes_field == 'mentions':
        if 'comment_id' in changes_value:
            return InstagramEventType.MENTION_IN_COMMENT
        return InstagramEventType.MENTION_IN_MEDIA
    return None


def process_messaging_event(message_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process messaging-related events using a mapping approach."""

    # Map message keys to their corresponding event types
    event_mapping: Dict[str, InstagramEventType] = {
        'postback': InstagramEventType.POSTBACK,
        'pass_thread_control': InstagramEventType.PASS_THREAD_CONTROL,
        'request_thread_control': InstagramEventType.REQUEST_THREAD_CONTROL,
        'read': InstagramEventType.MESSAGE_READ
    }

    # Check if any direct events are present
    for key, event_type in event_mapping.items():
        if key in message_value:
            return event_type

    if message_value.get('message', {}).get('reply_to', {}).get("story", None):
        reply_to = message_value['message']['reply_to']
        if 'story' in reply_to:
            return InstagramEventType.REPLY_TO_STORY
    reaction: Dict[str, Any] = message_value.get('reaction', {})
    reaction_mapping: Dict[str, InstagramEventType] = {
        'react': InstagramEventType.MESSAGE_REACT,
        'unreact': InstagramEventType.MESSAGE_UNREACT
    }
    if 'action' in reaction:
        return reaction_mapping.get(reaction['action'])
    message_data = message_value.get('message', {})
    if message_data.get('is_deleted', False):
        return InstagramEventType.MESSAGE_DELETED

    # Map attachment types to event types
    attachment_mapping: Dict[str, InstagramEventType] = {
        'video': InstagramEventType.MESSAGE_WITH_VIDEO,
        'unsupported_type': InstagramEventType.UNSUPPORTED_ATTACHMENT,
        'story_mention': InstagramEventType.STORY_MENTION,
        'template': InstagramEventType.MESSAGE_TEMPLATE
    }

    attachments: List[Dict[str, Any]] = message_value.get('message', {}).get('attachments', [])
    for attachment in attachments:
        attachment_type: Optional[str] = attachment.get('type')
        if attachment_type in attachment_mapping:
            return attachment_mapping[attachment_type]

    # Return MESSAGE type if 'message' exists in the payload
    return InstagramEventType.MESSAGE if 'message' in message_value else None


def process_standby_event(standby_value: Dict[str, Any]) -> Optional[InstagramEventType]:
    """Process standby-related events using a mapping approach."""

    # Map direct event keys to their corresponding event types
    event_mapping: Dict[str, InstagramEventType] = {
        'reaction': InstagramEventType.STANDBY_REACTION,
        'read': InstagramEventType.STANDBY_READ,
        'take_thread_control': InstagramEventType.STANDBY_TAKE_THREAD_CONTROL
    }

    # Check for direct events
    for key, event_type in event_mapping.items():
        if key in standby_value:
            return event_type

    # Check for message-related events
    message: Dict[str, Any] = standby_value.get('message', {})

    message_mapping: Dict[str, InstagramEventType] = {
        'reply_to': InstagramEventType.STANDBY_REPLY_TO_MESSAGE,
        'is_deleted': InstagramEventType.STANDBY_MESSAGE_DELETED,
        'text': InstagramEventType.STANDBY_SIMPLE_MESSAGE,
        'is_unsupported': InstagramEventType.STANDBY_UNSUPPORTED
    }

    for key, event_type in message_mapping.items():
        if key in message:
            return event_type

    # Process standby attachments
    attachments: List[Dict[str, Any]] = message.get('attachments', [])
    attachment_mapping: Dict[str, InstagramEventType] = {
        'image': InstagramEventType.STANDBY_MESSAGE_WITH_IMAGE,
        'video': InstagramEventType.STANDBY_MESSAGE_WITH_VIDEO,
        'unsupported_type': InstagramEventType.STANDBY_MESSAGE_WITH_UNSUPPORTED_ATTACHMENT,
        'share': InstagramEventType.STANDBY_MESSAGE_WITH_SHARE,
        'ig_reel': InstagramEventType.STANDBY_MESSAGE_WITH_REEL,
        'story_mention': InstagramEventType.STANDBY_STORY_MENTION,
        'audio': InstagramEventType.STANDBY_MESSAGE_WITH_AUDIO
    }

    for attachment in attachments:
        attachment_type: Optional[str] = attachment.get('type')
        if attachment_type in attachment_mapping:
            return attachment_mapping[attachment_type]

    return None


def classify_instagram_event(event_data):
    """Classify Instagram events based on the event data."""
    event = json.loads(event_data) if isinstance(event_data, str) else event_data
    try:
        changes = event.get('entry', [{}])[0]

        # Check if changes field exists
        changes_list = changes.get('changes', [{}])
        changes_field = changes_list[0].get('field', '')
        changes_value = changes_list[0].get('value', {})

        # Check for story insights
        if changes_field == 'story_insights':
            return InstagramEventType.STORY_INSIGHTS

        # Process media events
        media_event = process_media_event(changes_value)
        if media_event:
            return media_event

        # Process mentions
        mentions_event = process_mentions_event(changes_value, changes_field)
        if mentions_event:
            return mentions_event

        # Process messaging events
        if 'messaging' in changes:
            return process_messaging_event(changes['messaging'][0])

        # Process standby events
        if 'standby' in changes:
            return process_standby_event(changes['standby'][0])

        return None  # Return None if no match is found

    except KeyError as e:
        traceback.print_exc()
        print(f"KeyError: {e} for event is: {event}")
        return None
    except Exception as e:
        traceback.print_exc()
        print(f"Exception: {e} for event is: {event}")
        return None


if __name__ == "__main__":
    pass
    # data = [
    #     {"entry": [{"id": "17841401906857599", "time": 1726106088, "changes": [{"value": {
    #         "from": {"id": "2706325442860345", "username": "rachitsaini670"},
    #         "media": {"id": "17868660555124283", "media_product_type": "REELS"}, "id": "18058455121735594",
    #         "text": "7"}, "field": "comments"}]}], "object": "instagram"},
    #     {"object": "instagram", "entry": [
    #         {"time": 1726108555302, "id": "17841400361448203", "messaging": [
    #             {"sender": {"id": "5721598244550161"}, "recipient": {"id": "17841400361448203"},
    #              "timestamp": 1726108553241, "message": {
    #                 "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDAwMzYxNDQ4MjAzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1ODcxOTE0OTgyNzM5ODk2NzozMTg0MTA4MjcyNTA5MDAzMzQ0MjAwMTUxNjcyOTcyOTAyNAZDZD",
    #                 "attachments": [{"type": "ig_reel", "payload": {"reel_video_id": "17955123119699866",
    #                                                                 "title": "JUST KEEP GOING.\n.\n.\nauthenticvision: Is a brand that inspires and improves people's lives.\nJoin us on our journey. @authenticvision\n.\n.\n#authenticvision #motivation #mindset #wisdom #inspiration #motivational #inspirational #life #lifelessons #lessons #wisdom #qoutes #selfempowerment #selfempowerment #lambeturah #sony #nokia #lg #samsung #ikea",
    #                                                                 "url": "https:\\/\\/lookaside.fbsbx.com\\/ig_messaging_cdn\\/?asset_id=17955123119699866&signature=AbzkH0D7XG4e3ewdAAaVY-cKaF-wl4GEQ5cYHWAA5wCwtKoFZ-W_lVV-sW62uMXG0gfpH7uP8jUH4gDD5nKLOToeObWDsTDeEmUubXFkzwsmfcF3H2y5hAcWRuUVlzJyu3gdJrNwi5RMXYBRzC8Q7abWpKoevISp3Vg-JYqBC4WTP8ZUpUBZsQ94V_xWw_uQiOOWdlDTEOSPfz_KjAWsMWNoIYN93FY"}}]}}]}]},
    #
    #     {"object": "instagram", "entry": [{"time": 1726104851986, "id": "17841453859955858",
    #                                        "messaging": [{"sender": {"id": "17841453859955858"},
    #                                                       "recipient": {"id": "820748006894811"},
    #                                                       "timestamp": 1726104851311, "message": {
    #                                                "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDUzODU5OTU1ODU4OjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTU1NDEyNTUwNzIzMDEzMjozMTg0MTAxNDQzNjUyNzA1MjM2MjEyMjM2NjAyNzgyNTE1MgZDZD",
    #                                                "attachments": [{"type": "template", "payload": {
    #                                                    "generic": {"elements": [{
    #                                                        "title": "Hi! Thanks for your comment! \ud83d\ude80\n\nHere is your link \ud83d\udc47",
    #                                                        "buttons": [{
    #                                                            "type": "open_url",
    #                                                            "url": "https://my.manychat.com/r?act=95322ef3c493d3bae984d54ee2d355be&u=813604705&p=1196969&h=3ea802256c",
    #                                                            "title": "Click here!"}]}]}}}],
    #                                                "is_echo": True}}]}]},
    #
    #     # We can also identify the event if it is quick reply or not
    #     {"object": "instagram", "entry": [
    #         {"time": 1726105521193, "id": "17841401163137633", "messaging": [
    #             {"sender": {"id": "355813534163958"}, "recipient": {"id": "17841401163137633"},
    #              "timestamp": 1726105519738, "message": {
    #                 "mid": "aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDAxMTYzMTM3NjMzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTY5MTcxNzE0NjgxMzAxMjozMTg0MTAyNjc2NjgzNDY4MjQ5MDcwNDExNjI3NDE2NzgwOAZDZD",
    #                 "text": "How can I purchase your products?", "quick_reply": {
    #                     "payload": "3:IB_FIRST_PARTY:ac65f8133abf5df0f25b12575a30e397d9b057c2:no_response:is_custom"}}}]}]},
    #
    #     {'object': 'instagram', 'entry': [{'time': 1725785006797, 'id': '17841448359242263', 'messaging': [
    #         {'sender': {'id': '473277262230299'}, 'recipient': {'id': '17841448359242263'}, 'timestamp': 1725785006609,
    #          'message': {
    #              'mid': 'aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDQ4MzU5MjQyMjYzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI3NjIwMzIxMjM4OTMwNjM4NzozMTc4NDYwNTk3OTA5NDkxNDQ3MTMyOTQ1MTgwODM5MTE2OAZDZD',
    #              'is_deleted': True}}]}]},
    #     {'object': 'instagram', 'entry': [{'time': 1726300369484, 'id': '17841416674361805', 'messaging': [
    #         {'sender': {'id': '17841416674361805'}, 'recipient': {'id': '6394745907298910'}, 'timestamp': 1726300368829,
    #          'message': {
    #              'mid': 'aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDE2Njc0MzYxODA1OjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTA0NjY1MjY2MTMxMDU2NzozMTg0NDYyMTA5ODE0NDI2MzEzMjQ3MDE2NzYxODk3Nzc5MgZDZD',
    #              'attachments': [{'type': 'story_mention', 'payload': {
    #                  'url': 'https://lookaside.fbsbx.com/ig_messaging_cdn/?asset_id=18460564075058049&signature=AbwWwtb6HX98JT_6VAUmAP43MRfvtVm8s4aBobF1dw6FGVZixJNyBrnVRmjUjRmhMRVRPxs_1aOFvFPZz1TMEWoDh7p1_xaAj2W0aABEiEJfIfunK-KdXdqU9kbe0XMiHPH3oVhiTJhAjI7Y8Xqh0N4j3vop3OzZxD6HLYM0zc4u3jZNgrFGcpU7HgqvJHeMh6G_0gB70njyiFttg_Pa6_wzbZWcPlU'}}],
    #              'is_echo': True}}]}]},
    #     {'object': 'instagram', 'entry': [{'time': 1726326310628, 'id': '17841448359242263', 'messaging': [
    #         {'sender': {'id': '469726735841298'}, 'recipient': {'id': '17841448359242263'}, 'timestamp': 1726326309755,
    #          'message': {
    #              'mid': 'aWdfZAG1faXRlbToxOklHTWVzc2FnZAUlEOjE3ODQxNDQ4MzU5MjQyMjYzOjM0MDI4MjM2Njg0MTcxMDMwMTI0NDI1OTM5Njg4ODg2NjMxNTA2NzozMTg0NTA5OTYyMzc3MjgyNzk4MDY5MjUzOTE1OTA4NTA1NgZDZD',
    #              'text': 'i’m waiting for the giveawayyyyyyyyyyy\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79\ud83e\udd79',
    #              'reply_to': {'story': {
    #                  'url': 'https:\\/\\/lookaside.fbsbx.com\\/ig_messaging_cdn\\/?asset_id=17927261066947525&signature=Aby32t5RpD76Nztt8BF4Ug5yU_GFaF8-Gr2NpA30vrM-2SfOzQWlZPY8K0m46AdWyXmRVfr0dhON2gZo0PMA377sw-t8OjhaAmQX37tEJLKSNlLIwkSnvUo0SWBu-riXXwc-enClfoRPQC8CuX9oWPR1Ct01nC196I8RitH5Whv0igmffUuMQMH2aSe4zhfyIBb7U4FR1QD-lMLseEK77fgeo0OVDUo',
    #                  'id': '17927261066947525'}}}}]}]}
    # ]
    # for obj in data:
    #     instagram_event_type = classify_instagram_event(obj)
    #     print(instagram_event_type.event_type)
