# ***** NOT IN USE ******

import facebook
import requests
import json

access_token = "EAADrd2lpF3IBAKBZBpHl9zN2HJ4Yx7XrSrhVEc57Cs6znG2a9gWGB5ldQNyqaA3JI5hBWlU8KEA7DJhbMXxrReIbH6xuAoZBIf6MJ1p7Y8mbWZCA3iZBLP2aJxBvADFd2xQIZAmGj90JcRZAaqQ6se4paQbpreK7cZCgQWo9c5dl96OsRnlMH09flJpXpXZAZCU1IDKN1HDerBBN9rY8nxlZBRNdMP7OeryAiHRVvBWZCF7vAZDZD"

token_url = 'https://graph.facebook.com/oauth/access_token'
params = dict(client_id="258898102130546", client_secret="af59812fc1768de0c554200952b7a1fd", grant_type='client_credentials')
response = requests.get(url=token_url, params=params)
token = response.text
token_dict = json.loads(token)
access_token_get = token_dict['access_token']
graph = facebook.GraphAPI(access_token_get)
print(graph.get_object('Bill Gates'))


'''
class FacebookFeed:
    token_url = 'https://graph.facebook.com/oauth/access_token'
    params = dict(client_id=settings.SOCIAL_AUTH_FACEBOOK_KEY, client_secret=settings.SOCIAL_AUTH_FACEBOOK_SECRET,
                  grant_type='client_credentials')

    @classmethod
    def get_posts(cls, user, count=6):
        try:
            token_response = requests.get(url=cls.token_url, params=cls.params)
            access_token = token_response.text.split('=')[1]
            graph = facebook.GraphAPI(access_token)
            profile = graph.get_object(user)
            query_string = 'posts?limit={0}'.format(count)
            posts = graph.get_connections(profile['id'], query_string)
            return posts
        except facebook.GraphAPIError:
            return None
'''
