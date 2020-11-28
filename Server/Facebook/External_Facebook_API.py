from facebook_scraper import get_posts
import threading


class GroupCrawler(threading.Thread):
    def __init__(self, group, db_handler):
        threading.Thread.__init__(self)
        self._handler = db_handler
        self.group = group
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        credentials = ("mysavta.test1@gmail.com", "TempPassword123")

        for post in get_posts(group=self.group, pages=1, credentials=credentials):
            pass


def main():
    print("This is used for testing.")


if __name__ == '__main__':
    main()
