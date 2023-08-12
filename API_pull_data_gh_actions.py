import os
import pickle
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from src.utils_gh_actions import (
    get_creds,
    get_user_media,
    get_media_insights,
    get_user_insights,
    media_lists,
)

# Get path of current file
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")
os.makedirs(data_dir, exist_ok=True)

params = get_creds()
response_media = get_user_media(params)

# Get media metadata
media_type_list, caption_list, timestamp_list, id_list = media_lists(response_media)

flag = True
while flag == True:
    # Load data from the next page
    response_media = get_user_media(
        params, response_media["json_data"]["paging"]["next"]
    )

    # Store the page media information in a temporary list and update the list
    # storing all the media
    media_type_page, caption_page, timestamp_page, id_page = media_lists(response_media)
    media_type_list = media_type_list + media_type_page
    caption_list = caption_list + caption_page
    timestamp_list = timestamp_list + timestamp_page
    id_list = id_list + id_page

    # Check if there's another media page
    flag = "next" in response_media["json_data"]["paging"]

# Generate new columns using the date and time from the timestamp
timestamp_list = [
    datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z") for date in timestamp_list
]
date_list = [date.strftime("%Y-%m-%d") for date in timestamp_list]
time_list = [date.strftime("%H:%M:%S") for date in timestamp_list]
date_time_list = [date.strftime("%Y-%m-%d %H:%M:%S") for date in timestamp_list]


# Create a dataframe using the lists
media_metadata = pd.DataFrame(
    data=[id_list, media_type_list, date_time_list, date_list, time_list, caption_list]
).T.rename(
    columns={
        0: "media_id",
        1: "media_type",
        2: "date_time",
        3: "date",
        4: "time",
        5: "caption",
    }
)

# Save data
today_str = datetime.today().strftime("%Y_%m_%d")
media_metadata.to_csv(f"{data_dir}/media_metadata.csv", index=False)


# Media data
# Pre-allocate memory
photo_data = np.zeros((len(date_list), 5))
reel_data = np.zeros((len(date_list), 7))

for i, (media_type, id_val) in enumerate(zip(media_type_list, id_list)):
    # Get the media id and fetch data using the API
    params["media_id"] = id_val
    response = get_media_insights(params, media_type)

    # If the media is a VIDEO, the metrics relevant to the video will be updated
    # using the information from the json object
    # The metrics related to the PHOTO will be set to nan
    if media_type == "VIDEO":
        for j in range(7):
            reel_data[i, j] = response["json_data"]["data"][j]["values"][0]["value"]
        photo_data[i, :] = np.NAN
    # If the media is a PHOTO or CAROUSEL, the metrics relevant to the video will be updated
    # using the information from the json object
    # The metrics related to the VIDEO will be set to nan
    else:
        for j in range(5):
            photo_data[i, j] = response["json_data"]["data"][j]["values"][0]["value"]
        reel_data[i, :] = np.NAN

photo_df = pd.DataFrame(
    data=photo_data,
    columns=["engagement", "impressions", "reach", "saved", "video_views"],
)
photo_df["media_id"] = id_list

reel_df = pd.DataFrame(
    data=reel_data,
    columns=[
        "video_comments",
        "video_likes",
        "video_plays",
        "video_reach",
        "video_saved",
        "video_shares",
        "video_interactions",
    ],
)
reel_df["media_id"] = id_list

media_df = photo_df.merge(reel_df, left_on="media_id", right_on="media_id")

column_to_move = media_df.pop("media_id")
media_df.insert(0, "media_id", column_to_move)
media_df.insert(1, "media_type", media_type_list)

media_df.to_csv(f"{data_dir}/media insight/media_insight_{today_str}.csv", index=False)

# Profile insight
# Define interval for results
until_day = datetime.today().strftime("%Y-%m-%d")
days_data = 30
since_day = (datetime.today() - timedelta(days=days_data)).strftime("%Y-%m-%d")

since_day = int(datetime.strptime(since_day, "%Y-%m-%d").strftime("%s"))
until_day = int(datetime.strptime(until_day, "%Y-%m-%d").strftime("%s"))

# Define period type
period = "day"

response = get_user_insights(
    params, period, since_day, until_day
)  # get insights for a user

# Get the values from the json object
day_list = [x["end_time"] for x in response["json_data"]["data"][0]["values"]]
follower_list = [x["value"] for x in response["json_data"]["data"][0]["values"]]
impressions_list = [x["value"] for x in response["json_data"]["data"][1]["values"]]
prof_views_list = [x["value"] for x in response["json_data"]["data"][2]["values"]]
reach_list = [x["value"] for x in response["json_data"]["data"][3]["values"]]

# Create a dataframe containing the profile insight data
profile_insight = pd.DataFrame(
    data={
        "day": day_list,
        "number_followers": follower_list,
        "impressions": impressions_list,
        "profile_views": prof_views_list,
        "profile_reach": reach_list,
    }
)

# Change date format
profile_insight["day"] = profile_insight["day"].apply(
    lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S%z")
)
profile_insight["day"] = profile_insight["day"].apply(lambda x: x.strftime("%Y-%m-%d"))

# Sort values by date to have the
profile_insight.sort_values(by="day", ascending=False, inplace=True, ignore_index=True)

# Add new information to profile insight data file
old_prof_insight = pd.read_csv(f"{data_dir}/profile_insight.csv")

latest_day = old_prof_insight.query("number_followers == 0")["day"].iloc[-1]
latest_ind = old_prof_insight.loc[old_prof_insight["day"] == latest_day].index[0]

new_data = profile_insight.loc[profile_insight["day"] >= latest_day]

all_profile_insight = pd.concat(
    [new_data, old_prof_insight.iloc[(latest_ind + 1) :, :]]
).reset_index(drop=True)

all_profile_insight.to_csv(f"{data_dir}/profile_insight.csv", index=False)

# Define period type
period = "lifetime"

response = get_user_insights(params, period, since_day, until_day)

# Serialize the dictionary to a file
with open(
    f"{data_dir}/profile demographics/profile_demographics_{today_str}.pkl", "wb"
) as f:
    pickle.dump(response["json_data"]["data"], f)
