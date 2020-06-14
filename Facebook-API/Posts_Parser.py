from Facebook_API import get_posts_curl
import json


class haver():
    '''
    Constructor:
        Make new 'haver' object. If a post is parseable, then its assumed relevant, if not, then assume irrelevant.
    Arguments:
        entry: the post's json data. | type dictionary.
    Returns:
        New haver object. Check 'relevant' flag.
    '''
    def __init__(self, entry):
        try :
            #I will add support later
            self.fam_name = ''
            self.lang = ['hebrew']

            #taken from 'from' field.
            self.facebook_id = entry['from']['id']

            #first sentence should include other info. the second needs to contain the phone number.
            info = entry['message'].split('.')
            self.phone_number = extract_numbers(info[1])

            #extracting info from firts sentance.
            info = info[0].split(',')
            self.name = info[0].split(' ')[-1]
            self.age = int(extract_numbers(info[1]))
            self.city = ' '.join(info[2].split(' ')[2:])[1:].lower()
            if self.city.islower():
                self.city = self.city.split(' ')
                if len(self.city) == 3:
                    self.city = self.city[-1]
                elif len(self.city) == 4:
                    self.city = ' '.join(self.city[-2:])
            self.job = ' '.join(info[3].split(' ')[2:]).lower()
            if self.job.islower():
                self.job = ' '.join(self.job.split(' ')[2:])
            self.relevant = True
            print('Post relevant, registered')
        #if exception is raised then post isn't relevant.
        except :
            self.relevant = False
            print('Post not relevant, dropped.')

    '''
    Printing Function:
        This function will enable the function 'print' to print this object.
    Arguments:
        None.
    Return:
        A string with all the information needed to be displayed.
    '''
    def __str__(self):
        return 'Name: ' + self.name + "   Age:" + str(self.age) + '   Location: ' + self.city + '   Job: ' + self.job + '.'

'''
Function:
    This function will extract only the numbers from a string.
Arguments:
    string: a string. | type: str.
Return:
    String containing only numbers.
'''
def extract_numbers(string):
    res = ''
    for char in string:
        if char.isdigit():
            res += char
    return res

'''
Function:
    This function will parse and construct 'haver' objects.
Arguments:
    curl: a json object containing Facebooks' response. | type: str.
Return: list of new 'haver' objects. | type: [haver, ].
'''
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
        #print(post)
        if new_entry.relevant:
            list_haverim.append(new_entry)

    return list_haverim


if __name__=='__main__':
    curl = get_posts_curl()
    new_haverim = get_haverim_from_posts(curl)
    if new_haverim != None:
        for haver in new_haverim:
            print(haver)