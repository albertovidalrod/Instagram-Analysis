from defines import get_creds, make_api_call

def get_user_media( params, pagingUrl = '' ) :
	""" Get users media
	
	API Endpoint:
		https://graph.facebook.com/{graph-api-version}/{ig-user-id}/media?fields={fields}&access_token={access-token}

	Returns:
		object: data from the endpoint

	"""

	endpoint_params = dict() # parameter to send to the endpoint
	endpoint_params['fields'] = 'id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username' # fields to get back
	endpoint_params['access_token'] = params['access_token'] # access token

	if ( '' == pagingUrl ) : # get first page
		url = params['endpoint_base'] + params['instagram_account_id'] + '/media' # endpoint url
	else : # get specific page
		url = pagingUrl  # endpoint url

	return make_api_call( url, endpoint_params, params['debug'] ) # make the api call

params = get_creds() # get creds
params['debug'] = 'no' # set debug
response = get_user_media( params ) # get users media from the api

print("\n\n---------- POST ----------\n") # post heading
print("Link to post:") # label
print(response['permalink']) # link to post
print("\nPost caption:") # label
print(response['caption']) # post caption
print("\nMedia type:") # label
print(response['media_type']) # type of media
print("\nPosted at:") # label
print(response['timestamp']) # when it was posted

# print("\n\n\n\t\t\t >>>>>>>>>>>>> >>>>>>> PAGE 1 <<<<<<<<<<<<<<<<<<<<\n") # display page 1 of the posts

# for post in response['json_data']['data'] :
# 	print "\n\n---------- POST ----------\n" # post heading
# 	print "Link to post:" # label
# 	print post['permalink'] # link to post
# 	print "\nPost caption:" # label
# 	print post['caption'] # post caption
# 	print "\nMedia type:" # label
# 	print post['media_type'] # type of media
# 	print "\nPosted at:" # label
# 	print post['timestamp'] # when it was posted

# params['debug'] = 'no' # set debug
# response = getUserMedia( params, response['json_data']['paging']['next'] ) # get next page of posts from the api

# print "\n\n\n\t\t\t >>>>>>>>>>>>>>>>>>>> PAGE 2 <<<<<<<<<<<<<<<<<<<<\n" # display page 2 of the posts

# for post in response['json_data']['data'] :
# 	print "\n\n---------- POST ----------\n" # post heading
# 	print "Link to post:" # label
# 	print post['permalink'] # link to post
# 	print "\nPost caption:" # label
# 	print post['caption'] # post caption
# 	print "\nMedia type:" # label
# 	print post['media_type'] # type of media
# 	print "\nPosted at:" # label
# 	print post['timestamp'] # when it was posted