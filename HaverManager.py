"""
Written by Maor Gelman
Date: 30/04/2020
"""

import sqlite3
from sqlite3 import Error
from random import randrange

PATH_TO_DB = "haverim.db"

def startConnection():
    try:
        conn = sqlite3.connect(PATH_TO_DB)
        c = conn.cursor()
        return c, conn

    except Error as e:
        print(e)
        return None, None

def createLanguagesStr(languages):
    languages_str = "("
    languages_list = languages.split(", ")
    for i in range(len(languages_list)):
        if i == len(languages_list) - 1:
            languages_str += "LANGUAGES LIKE '%{}%'".format(languages_list[i])
        else:
            languages_str += "LANGUAGES LIKE '%{}%' or ".format(languages_list[i])

    languages_str += ")"

    return languages_str


def getRandomIndex(length):
    return randrange(length)



def getHaver(location, languages, subject):
    c, conn = startConnection()

    if not conn is None:
        c.execute("SELECT * FROM HAVER WHERE Citi='{}' and Employement LIKE '%{}%' and {}".format(location,subject, createLanguagesStr(languages)))
        rows = c.fetchall()
        print(rows)

        if len(rows) == 0:
            subject = "General"
            c.execute("SELECT * FROM HAVER WHERE Citi='{}' and Employement LIKE '%{}%' and {}".format(location,subject, createLanguagesStr(languages)))
            rows = c.fetchall()
            print(rows)

            if len(rows) == 0:
                return None

        conn.close()
        return rows[getRandomIndex(len(rows))] #the function will find the best match in the next version

    return None


#if __name__ == "__main__":
 #   getHaver("Ramat-Gan", 'hebrew, russian', "Computers")
