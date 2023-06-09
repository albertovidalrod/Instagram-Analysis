from defines import get_creds, make_api_call

def getInstagramAccount( params ) :
	""" Get instagram account
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{page-id}?access_token={your-access-token}&fields=instagram_business_account
	Returns:
		object: data from the endpoint
	"""

	endpoint_params = dict() # parameter to send to the endpoint
	endpoint_params['access_token'] = params['access_token'] # tell facebook we want to exchange token
	endpoint_params['fields'] = 'instagram_business_account' # access token

	url = params['endpoint_base'] + params["page_id"]# endpoint url

	return make_api_call( url, endpoint_params, params['debug'] ) # make the api call

params = get_creds() # get creds
params['debug'] = 'no' # set debug
response = getInstagramAccount( params ) # get debug info

print("\n---- INSTAGRAM ACCOUNT INFO ----\n")
print("Page Id:") # label
print(response['json_data']['id']) # display the page id
print("\nInstagram Business Account Id:") # label
print(response['json_data']['instagram_business_account']['id']) #display the instagram account id