import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()


def get_creds():
    creds = dict()
    creds["access_token"] = os.getenv("access_token")
    creds["client_id"] = os.getenv("client_id")
    creds["client_secret"] = os.getenv("client_secret")
    creds["graph_domain"] = "https://graph.facebook.com/"
    creds["graph_version"] = "v16.0"
    creds["endpoint_base"] = creds["graph_domain"] + creds["graph_version"] + "/"
    creds["page_id"] = os.getenv("page_id")
    creds["instagram_account_id"] = os.getenv("instagram_account_id")
    creds["ig_username"] = os.getenv("ig_username")
    creds["debug"] = "no"
    return creds


def make_api_call(url, endpoint_params, debug="no"):
    data = requests.get(url, params=endpoint_params)
    response = dict()
    response["url"] = url
    response["endpoint_params"] = endpoint_params
    response["endpoint_params_pretty"] = json.dumps(endpoint_params, indent=4)
    response["json_data"] = json.loads(data.content)
    response["json_data_pretty"] = json.dumps(response["json_data"], indent=4)

    if debug == "yes":
        display_api_call_data(response)

    return response


def display_api_call_data(response):
    print("\nURL: ")
    print(response["url"])
    print("\nEndpoint params: ")
    print(response["endpoint_params_pretty"])
    print("\nResponse:  ")
    print(response["json_data_pretty"])


def get_info_account(params):
    """Get info on a users account

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}?fields=business_discovery.username({ig-username})
            {username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}
            &access_token={access-token}

    Returns:
        object: data from the endpoint

    """

    endpoint_params = dict()  # parameter to send to the endpoint
    endpoint_params["fields"] = (
        "business_discovery.username("
        + params["ig_username"]
        + ")\
        {username,website,name,ig_id,id,profile_picture_url,biography,follows_count,followers_count,media_count}"
    )  # string of fields to get back with the request for the account
    endpoint_params["access_token"] = params["access_token"]  # access token

    url = params["endpoint_base"] + params["instagram_account_id"]  # endpoint url

    return make_api_call(url, endpoint_params, params["debug"])  # make the api call


def get_user_media(params, pagin_url=""):
    """Get users media

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}

    Returns:
        object: data from the endpoint
    """

    endpoint_params = dict()  # parameter to send to the endpoint
    endpoint_params[
        "fields"
    ] = "id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username"  # fields to get back
    endpoint_params["access_token"] = params["access_token"]  # access token

    if "" == pagin_url:  # get first page
        url = (
            params["endpoint_base"] + params["instagram_account_id"] + "/media"
        )  # endpoint url
    else:  # get specific page
        url = pagin_url  # endpoint url

    return make_api_call(url, endpoint_params, params["debug"])  # make the api call


def get_media_insights(params, media_type):
    """Get insights for a specific media id

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-media-id}/insights?metric={metric}

    Returns:
        object: data from the endpoint

    """
    if media_type == "VIDEO":  # media is a video
        params["metric"] = "comments,likes,plays,reach,saved, shares,total_interactions"
    elif media_type == "CAROUSEL_ALBUM":
        params["metric"] = (
            "carousel_album_engagement, carousel_album_impressions, "
            "carousel_album_reach, carousel_album_saved, carousel_album_video_views"
        )  # media is a carousel album
    elif media_type == "PHOTO":  # media is an image
        params["metric"] = "engagement,impressions,reach,saved"

    endpoint_params = dict()  # parameter to send to the endpoint
    endpoint_params["metric"] = params["metric"]  # fields to get back
    endpoint_params["access_token"] = params["access_token"]  # access token

    url = params["endpoint_base"] + params["media_id"] + "/insights"  # endpoint url

    return make_api_call(url, endpoint_params, params["debug"])  # make the api call


def get_user_insights(params, period="day", since_day="", until_day=""):
    """Get insights for a users account

    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/{ig-user-id}/insights?metric={metric}&period={period}&since={since}&until={until}
    Returns:
        object: data from the endpoint
    """

    endpoint_params = dict()  # parameter to send to the endpoint
    # Different period values return different metrics
    # define params if the user sets period equal to "day"
    if period == "day":
        endpoint_params[
            "metric"
        ] = "follower_count,impressions,profile_views,reach"  # fields to get back
        endpoint_params["period"] = period  # period
        endpoint_params["since"] = since_day
        endpoint_params["until"] = until_day
        endpoint_params["access_token"] = params["access_token"]  # access token

    # define params if the user sets the period equal to "lifetime"
    elif period == "lifetime":
        endpoint_params[
            "metric"
        ] = "audience_city,audience_country,audience_gender_age,audience_locale"  # fields to get back
        endpoint_params["period"] = period  # period
        endpoint_params["access_token"] = params["access_token"]  # access token

    url = (
        params["endpoint_base"] + params["instagram_account_id"] + "/insights"
    )  # endpoint url

    return make_api_call(url, endpoint_params, params["debug"])  # make the api call


def media_lists(response_media):
    """
    Store the information from different posts in lists

    Args:
        - response_media: json obejct containing information about posts

    Returns:
        - media_type_list: list containing the media type
        - caption_list: list contianing the caption
        - timestamp: list containing the timestamp of the media
        - id_list: list containing the media id
    """

    media_type_list = [
        media_data["media_type"] for media_data in response_media["json_data"]["data"]
    ]
    caption_list = [
        media_data["caption"] for media_data in response_media["json_data"]["data"]
    ]
    timestamp_list = [
        media_data["timestamp"] for media_data in response_media["json_data"]["data"]
    ]
    id_list = [media_data["id"] for media_data in response_media["json_data"]["data"]]

    return media_type_list, caption_list, timestamp_list, id_list
