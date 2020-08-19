import threading
import time
from Facebook.Posts_Parser import get_haverim_from_facebook
from Haverim_DB.DB_Handler import database_handler


class facebook_crawler(threading.Thread):
    def __init__(self, time_between_checks):
        threading.Thread.__init__(self)
        self.time = time_between_checks
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        print('Facebook thread started successfully. - facebook')
        last_check = time.time()
        handler = database_handler(host='192.168.1.26', password='AnthonNaivelt123')
        new_haverim = None
        last_post = ''

        while True:
            if time.time() - last_check > self.time:
                last_check = time.time()

                try:
                    print('Trying to parse posts from facebook. - facebook.')
                    new_haverim, last_post = get_haverim_from_facebook(last_post)
                    print('Done. - facebook')

                except ValueError:
                    pass

                except KeyboardInterrupt:
                    return

                if new_haverim is not None:
                    for haver in new_haverim:
                        print('New haver added: {}. - facebook'.format(haver))
                        handler.add_haver_to_db(haver)
                    print('New haverim committed to db. - facebook')
                    handler.commit()
