import json
from typing import List, Optional


async def extracting_parent_post_for_comments(clickhouse_obj, parent_post_id: str, post_author_id, category_ids: str,
                                              brand_ids: str, channel_group_id: int) -> Optional[List[dict]]:
    """
    This function fetches the parent post from the ClickHouse database.
    Post author id is required to check if the comment is from the brand or not.
    If yes, then we need to map the parent user details to the comments as well.
    """
    clickhouse_query = f"""
        SELECT tweetidorfbid, url, instagramgraphapiid, u_followerscount, u_followingcount, u_tweetcount, u_authorid, isbrandpost
        FROM spatialrss.mentiondetails  final
        PREWHERE categoryid IN ({category_ids}) AND brandid IN ({brand_ids}) 
        WHERE channelgroupid={channel_group_id} AND tweetidorfbid='{parent_post_id}'
    """

    clickhouse_obj.execute(clickhouse_query)
    df = clickhouse_obj.fetch_df()

    if df.empty:
        return None

    field_mapping = {
        "u_followerscount": "comment_follower_count",
        "u_followingcount": "comment_follows_count",
        "u_tweetcount": "comment_tweet_count",
        "url": "parent_post_url",
        "tweetidorfbid": "parent_post_social_id",
        "isbrandpost": "is_parent_brand_post",
    }

    result_list = []

    for _, row in df.iterrows():
        # Handle the `isbrandpost` logic
        is_brand_post = row.get("isbrandpost", None)

        if is_brand_post is None or is_brand_post == "":
            is_brand_post = False  # Treat null or empty as False
        elif isinstance(is_brand_post, (int, bool)):
            is_brand_post = bool(is_brand_post)  # Convert 0/1 to False/True

        # Mapping fields
        mapped_row = {field_mapping.get(k, k): v for k, v in row.items() if k in field_mapping}

        # Set the processed `is_brand_post`
        mapped_row["is_brand_post"] = is_brand_post

        # If the author matches the post author id, map all fields, otherwise, only map `url` and `tweetidorfbid`
        if row["u_authorid"] == post_author_id:
            result_list.append(mapped_row)
        else:
            result_list.append({k: mapped_row[k] for k in ["parent_post_url", "parent_post_social_id", "is_parent_brand_post"]})

    return result_list


async def call_api_to_get_parent_post_details(post_id, instagram_api, access_token, post_fields_attributes, logger):
    response_data = await instagram_api.fetch_instagram_data(
        endpoint=post_id,
        access_token=access_token,
        logger=logger,
        fields=post_fields_attributes

    )
    if response_data and isinstance(response_data, str):
        response_data = json.loads(response_data)

    return response_data
