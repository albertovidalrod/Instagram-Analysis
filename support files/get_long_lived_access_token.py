from defines import get_creds, make_api_call


def get_long_lived_access_token( params ):
    """ Get long lived access token
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}
	Returns:
		object: data from the endpoint
	"""
    endpoint_params = dict()
    endpoint_params["grant_type"] = "fb_exchange_token"
    endpoint_params["client_id"] = params["client_id"]
    endpoint_params["client_secret"] = params["client_secret"]
    endpoint_params["fb_exchange_token"] = params["access_token"]

    url = params['endpoint_base'] + 'oauth/access_token' # endpoint url

    return make_api_call( url, endpoint_params, params['debug'] ) # make the api call


params = get_creds() # get creds
params['debug'] = 'yes' # set debug
response = get_long_lived_access_token( params ) # hit the api for some data!

print("\n ---- ACCESS TOKEN INFO ----\n") # section header
print("Access Token:")  # label
print(response['json_data']['access_token'])# display access token