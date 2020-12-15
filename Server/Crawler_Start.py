from Facebook.External_Facebook_API import GroupCrawler
from Haverim_DB.DB_Handler import DatabaseHandler


# Insert names or IDs of groups that you would like to scrape
GROUPS = ["879404338742203", "1244613082279475", "148441651998410", "Israel.Volunteering"]


def main():
    group_list = GROUPS
    handler = DatabaseHandler(host="localhost", user="root", password="cleo_anthon_123")
    group_crawler_object = GroupCrawler(None, handler)

    for group in group_list:
        print("Starting scraping group: ", group)
        group_crawler_object.group = group
        group_crawler_object.scrape()


if __name__ == '__main__':
    main()
