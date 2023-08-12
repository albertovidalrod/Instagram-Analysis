from defines import get_creds, make_api_call
import datetime


def debug_access_token(params):
    """Get info on an access token

    API Endpoint:
            https://graph.facebook.com/debug_token?input_token={input-token}&access_token={valid-access-token}
    Returns:
            object: data from the endpoint
    """

    endpoint_params = dict()
    endpoint_params["input_token"] = params["access_token"]
    endpoint_params["access_token"] = params["access_token"]

    url = params["graph_domain"] + "/debug_token"

    return make_api_call(url, endpoint_params, params["debug"])


params = get_creds()
params["debug"] = "yes"
response = debug_access_token(params)

print("\nData Access Expires at: ")  # label
print(
    datetime.datetime.fromtimestamp(
        response["json_data"]["data"]["data_access_expires_at"]
    )
)  # display out when the token expires

print("\nToken Expires at: ")  # label
print(
    datetime.datetime.fromtimestamp(response["json_data"]["data"]["expires_at"])
)  # display out when the token expires
