from Facebook_API import get_posts_curl
import json
import threading
import sqlite3
from sqlite3 import Error
import time

PATH_TO_DB = "haverim.db"

def startConnection():
    try:
        conn = sqlite3.connect(PATH_TO_DB)
        c = conn.cursor()
        return c, conn

    except Error as e:
        print(e)
        return None, None

class haver:
    def __init__(self, entry):
        try :
            #I will add support later
            self.last_name = ''
            self.lang = ['hebrew']

            #taken from 'from' field.
            self.facebook_id = entry['from']['id']

            #first sentence should include other info. the second needs to contain the phone number.
            info = entry['message'].split('.')
            self.phone_number = filter_phone_number(info[1])

            #extracting info from firts sentance.
            info = info[0].split(',')
            self.name = info[0].split(' ')[-1]
            self.age = int(filter_phone_number(info[1]))
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


    def __str__(self):
        return 'Name: ' + self.name + "   Age:" + str(self.age) + '   Location: ' + self.city + '   Job: ' + self.job + '.'


def filter_phone_number( number):
    res = ''
    for char in number:
        if char.isdigit():
            res += char
    return res


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


def getHaverimFromFacebook():
    curl = get_posts_curl()
    new_haverim = get_haverim_from_posts(curl)
    if not new_haverim is None:
        return new_haverim
    return None

def insertHaverToDb(haver):
    try:

        sqlite_insert_query = """ INSERT INTO 'HAVER'('name', 'surname', 'email', 'phone', 'Age', 'Citi', 'street', 'building', 'LANGUAGES', 'Employement', 'Skills') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

        c, conn = startConnection()

        # Convert data into tuple format
        data_tuple = (haver.name, haver.last_name, "example@gmail.com", haver.phone_number, haver.age, haver.city, "", "", haver.lang, haver.job, "None")

        c.execute(sqlite_insert_query, data_tuple)

        conn.commit()
        print("The data inserted successfully to the USERS table")

    except:
        print("Failed to insert data into sqlite table")
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")

class FacebookManager(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            haverim = getHaverimFromFacebook()
            if not haverim is None:
                for haver in haverim:
                    insertHaverToDb(haver)

            time.sleep(60) #60 secondes between every check
