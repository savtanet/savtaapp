import socket
import threading
import json
import sys
import sqlite3

from HaverManager import *
"""
Written by Sean Chen
Date: 28/04/2020 
"""

#######################################
LIST_WORDS = []
DB_NAME = "SAVTAS.db"
#######################################

# reads the words from the file
def get_words():
    global LIST_WORDS
    try:
        with open("words", "r") as word_file:
            LIST_WORDS = word_file.readlines()
    except Exception as e:
        print("ERROR:", e)
        sys.exit(1)


def indentify_word(msg):
    words = msg.split(" ")

    # running on all the words in the msg
    for word in words:
        # checking if the word matches to any of the words in the word list
        for option in LIST_WORDS:
            # if match was found, returning the correct type of help
            # option = fire:policeman
            # see file <words>
            if len(word) > 2 and word in option:
                print(option.split(":")[1])
                return option.split(":")[1]

    return "general"



def clientMsgHandler(clientMsg):
    msgToClient = ""
    get_words()

    msg = clientMsg.split(":")  # decoding

    savtas_name = msg[0]
    savtas_request = msg[1]

    help_type = indentify_word(savtas_request)

    msgForClient = build_msg(savtas_name, help_type)  # building the json msg
    print(msgForClient)
    haverInfo = getHaver(msgForClient["city"], msgForClient["language"], msgForClient["type"])

    if haverInfo is None:
        msgToClient = "None"
    else:
        # msg - first_name:last_name:email:phone
        msgToClient = haverInfo[1] + ":" + haverInfo[2] + ":" + haverInfo[3] + ":" + haverInfo[4]

    return msgToClient


def build_msg(username, help_type):
    msg = {}
    msg["city"], msg["language"] = get_db_data(username)
    msg["username"] = username
    msg["type"] = help_type[:-1]  # removing the "\n"
    return msg


def get_db_data(username):
    try:
        with sqlite3.connect(DB_NAME) as con:
            cur = con.cursor()
            cur.execute("""select * from SAVTAS where Name='{}'""".format(username))
            data = cur.fetchone()
            return data[4], data[5]

    except Exception as e:
        print("exception {}".format(e))
        return "Unknown", "Unknown", "Unknown"
