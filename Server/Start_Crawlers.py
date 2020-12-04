from Facebook.External_Facebook_API import GroupCrawler
from Haverim_DB.DB_Handler import DatabaseHandler


GROUPS = ["879404338742203", "1244613082279475", "148441651998410", "Israel.Volunteering"]


def main():
    thread_list = []
    group_list = GROUPS
    handler = DatabaseHandler(host="localhost")

    for group in group_list:
        thread_list.append(GroupCrawler(group, handler))

    for thread in thread_list:
        thread.t.join()


if __name__ == '__main__':
    main()
