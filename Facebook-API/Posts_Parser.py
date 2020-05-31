from Facebook_API import get_posts_curl
import json


class haver():
    def __init__(self, entry):
        try :
            self.name = entry['from']['name']
            self.facebook_id = entry['from']['id']

            info = entry['message'].split('-')
            self.age = int(info[0])
            self.city = info[1]
            self.email = info[2]
            self.phone = info[3]
            self.ocupation = info[4]
            self.languages = info[5:]

            self.relevant = True
        except :
            self.relevant = False
            print('Post not relevant, dropped.')
            

def get_haverim_from_posts(curl):
    list_posts = json.loads(curl)
    list_haverim = []

    try :
        list_posts = list_posts['posts']['data']
    except:
        print('Error, token expired.')
        return None

    for post in list_posts:
        new_entry = haver(post)
        if new_entry.relevant:
            list_haverim.append(new_entry)

    return list_haverim


if __name__=='__main__':
    curl = get_posts_curl()
    new_haverim = get_haverim_from_posts(curl)
    print(new_haverim[0].email)