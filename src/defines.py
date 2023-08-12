import requests
import json
import os

from dotenv import load_dotenv

load_dotenv()


def get_creds():
    creds = dict()
    # the first token is originally generated in the meta app
    # creds["access_token"] = "EAAyaGN85nrEBAI7GjtpU1LjZBuq0Ix59rEqWySf6QCzVhaVTg9Qgwb2vuTXVCeufFKwBAohGcOB9p1dwIJrNZBw8ZAKRYURvdibJ75XW8KY0SxHhkf7J6AGSFpJLCcGnG0lzj8qfVytl0wedwBSujzoijhg5vNgjJMDBWDCk3ut9uIZBDS1RX546QLbsw5aBmJ0sPX8cJrpGD1aqAVza"
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
