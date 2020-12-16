# ***** NOT IN USE ******

import facebook
import requests
import json

# This token is good till 20201
access_token = "EAADrd2lpF3IBAKBZBpHl9zN2HJ4Yx7XrSrhVEc57Cs6znG2a9gWGB5ldQNyqaA3JI5hBWlU8KEA7DJhbMXxrReIbH6xuAoZBIf6MJ1p7Y8mbWZCA3iZBLP2aJxBvADFd2xQIZAmGj90JcRZAaqQ6se4paQbpreK7cZCgQWo9c5dl96OsRnlMH09flJpXpXZAZCU1IDKN1HDerBBN9rY8nxlZBRNdMP7OeryAiHRVvBWZCF7vAZDZD"

# Test1
token_url = 'https://graph.facebook.com/oauth/access_token'
params = dict(client_id="258898102130546", client_secret="af59812fc1768de0c554200952b7a1fd", grant_type='client_credentials')
response = requests.get(url=token_url, params=params)
token = response.text
token_dict = json.loads(token)
access_token_2 = token_dict['access_token']
graph = facebook.GraphAPI(access_token_2)
# print(graph.get_object('nintendo'))

# Test2 - works
graph2 = facebook.GraphAPI()
access_token_3 = graph2.get_app_access_token(app_id="258898102130546", app_secret="af59812fc1768de0c554200952b7a1fd")
print(access_token_3) # 258898102130546|pMADB8ULX1-bfw5cuOiLoK7Ocjw
auth_grath = facebook.GraphAPI(access_token_3)
posts = auth_grath.get_object("258898102130546")
print(posts)


# just need to get user ID and its GG
