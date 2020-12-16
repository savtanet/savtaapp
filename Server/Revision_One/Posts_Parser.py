# ***** NOT IN USE ******

import json
from Text_Parsing.Parse_Text_Params import parse_post_class_haver
from Revision_One.Parse_Text_W2V import calculate_diff, calculate_paragraph
from Revision_One.Facebook_API import get_posts_curl


def get_haverim_from_facebook(last_post):
    """
    Description: This function will manage the whole process of getting new haverim from facebook.
    Input: None
    Output: If the function found new haverim, returns a list of 'haver' object, else, none.
    """
    curl = get_posts_curl()
    new_haverim, last_post = get_haverim_from_posts(curl, last_post)
    if new_haverim is None or new_haverim is []:
        return None, last_post
    else:
        return new_haverim, last_post


def get_haverim_from_posts(curl, last_post):
    list_posts = json.loads(curl)
    list_haverim = []
    newest_post_in_batch_id = last_post
    newest_post_in_batch = True

    try:
        print('Trying to un-load posts from facebook. - parser')
        list_posts = list_posts['posts']['data']

    except KeyError:
        print('Un-loading fail. Error, token expired. - parser')
        raise ValueError('Error, token expired.')

    print('Last post is: {}    Newest post is: {}. - parser'.format(last_post, list_posts[0]['id']))
    for post in list_posts:
        if post['id'] == last_post:
            print('No new posts.')
            break

        if newest_post_in_batch:
            newest_post_in_batch = False
            newest_post_in_batch_id = post['id']

        new_entry = parse_post_class_haver(post['message'])
        if new_entry is not None and calculate_diff(calculate_paragraph(post['message'])):
            print('Post relevant. Adding: {}. - parser'.format(new_entry))
            new_entry.facebook_id = post['from']['id']
            list_haverim.append(new_entry)

        else:
            print("Post isn't relevant. - parser")

    return list_haverim, newest_post_in_batch_id
