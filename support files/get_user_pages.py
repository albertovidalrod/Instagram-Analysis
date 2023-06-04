from defines import get_creds, make_api_call

def get_user_pages( params ) :
	""" Get facebook pages for a user
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/me/accounts?access_token={access-token}
	Returns:
		object: data from the endpoint
	"""

	endpoint_params = dict() # parameter to send to the endpoint
	endpoint_params['access_token'] = params['access_token'] # access token

	url = params['endpoint_base'] + 'me/accounts' # endpoint url

	return make_api_call( url, endpoint_params, params['debug'] ) # make the api call

params = get_creds() # get creds
params['debug'] = 'yes' # set debug
response = get_user_pages(params) # get debug info

print("\n---- FACEBOOK PAGE INFO ----\n") # section heading
print("Page Name:") # label
print(response['json_data']['data'][0]['name']) # display name
print("\nPage Category:") # label
print(response['json_data']['data'][0]['category']) # display category
print("\nPage Id:") # label
print(response['json_data']['data'][0]['id']) # display id