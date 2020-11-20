from facebook_scraper import get_posts


def get_page_post_generator(url, number_of_pages=1, credentials=("mysavta.test1@gmail.com", "TempPassword123")):
    return get_posts(url, pages=number_of_pages, credentials=credentials)


def get_group_post_generator(group, number_of_pages=1, credentials=("mysavta.test1@gmail.com", "TempPassword123")):
    return get_posts(group=group, pages=number_of_pages, credentials=credentials)


# Doesn't work for users.
def get_user_post_generator(user_id, number_of_pages=1, credentials=("mysavta.test1@gmail.com", "TempPassword123")):
    return get_posts(user_id, pages=number_of_pages, credentials=credentials)


gen = get_group_post_generator("Israel.Volunteering", number_of_pages=1)
for post in gen:
    print(post['user_id'])
