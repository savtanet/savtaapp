# -*- coding: utf-8 -*-
import threading
import time
from Haverim_DB.haverim_class import Haver
from facebook_scraper import get_posts
from deep_translator import GoogleTranslator
from Text_Parsing import NPL_Engine
from Text_Parsing.Parse_Text_Params import clean_post


from Haverim_DB.DB_Handler import DatabaseHandler


class GroupCrawler:
    def __init__(self, group, db_handler):
        self._handler = db_handler
        self.group = group
        self._translator = GoogleTranslator(source='iw', target='en')

    def scrape(self):
        # credentials = ("mysavta.test1@gmail.com", "TempPassword123")
        # This lists will contain post related values.
        translated_posts = []
        user_id_list = []

        # This lists will contain NLP related values.
        bow_list = []
        score_list = []

        for post in get_posts(group=self.group, pages=10):
            text = clean_post(post['text'])
            user_id = str(post['user_id'])
            if text != "" and user_id is not None and user_id != "None":
                time.sleep(0.2)
                translated_posts.append(self._translator.translate(text))
                user_id_list.append(str(post['user_id']))

        for translated_post in translated_posts:
            bow_list.append(NPL_Engine.make_bag_of_words(translated_post))
            score_list.append(NPL_Engine.calculate_bow_relation_to_cluster(bow_list[-1]))

        for score, facebook_id in zip(score_list, user_id_list):
            if score > NPL_Engine.HAVER_THRESHOLD:
                new_haver = Haver(facebook_id)
                self._handler.add_haver_to_db(new_haver)
                self._handler.commit()

        return user_id_list


def main():
    crawler = GroupCrawler("Israel.Volunteering", DatabaseHandler(host="localhost",
                                                                  user="root",
                                                                  password="cleo_anthon_123"))
    ids = crawler.scrape()
    print(ids)


if __name__ == '__main__':
    main()
