from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from Posts_Parser import haver, get_haverim_from_posts
from Facebook_API import get_posts_curl


engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base(bind=engine)
Base.metadata.create_all()
Session = sessionmaker(bind=engine)
s = Session()


class haver_sql(Base):
    __tablename__ = 'haverim' 
    id = Column(Integer, primary_key=True)
    facebook_id = Column(Integer)
    name = Column(Unicode(16))
    age = Column(Integer)
    city = Column(Unicode(32))
    job = Column(Unicode(64))
    phone = Column(Unicode(12))


    def __init__(self, haverObj):
        self.facebook_id = haverObj.facebook_id
        self.name = haverObj.name
        self.age = haverObj.age
        self.city = haverObj.city
        self.job = haverObj.job
        self.phone = haverObj.phone_number


def convert_haver_to_sql(haverim_list):
    haverim_sql_list = []
    for obj in haverim_list:
        new_entry = haver_sql(obj)
        haverim_sql_list.append(new_entry)
    return haverim_sql_list


def commit_new_haverim(haverim_list, sql_session):
    haverim_sql_list = convert_haver_to_sql(haverim_list)
    sql_session.add_all(haverim_sql_list)
    sql_session.commit()


if __name__ == '__main__':
    curl = get_posts_curl()
    new_haverim = get_haverim_from_posts(curl)
    if new_haverim != None:
        for haver in new_haverim:
            print(haver)
        commit_new_haverim(new_haverim, s)
        