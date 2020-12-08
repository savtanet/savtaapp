import mysql.connector
from Haverim_DB.haverim_class import Haver


class DatabaseHandler:
    def __init__(self, password=None, host='localhost', user='root', database='development'):
        if password is None:
            password = input("Please enter your MySQL user password: ")
        print('Attempting to connect to MySQL data base. - db handler')
        self.db = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.db.cursor()
        self.cursor.execute('USE ' + database)
        print('Connected to MySQL data base. - db handler')

    def add_haver_to_db(self, haver_object):
        insert_haver_formula = "INSERT INTO Haver" \
                               " (facebook_id)" \
                               " VALUES (%s)"
        try:
            self.cursor.execute(insert_haver_formula, haver_object.to_tuple())
        except mysql.connector.errors.IntegrityError:
            print("Duplicate")
            pass

    def add_haver_cert_to_db(self, haver_cert_object):
        insert_haver_cert_formula = "INSERT INTO HaverCertified" \
                                    " (name, location, phone, facebook_id, email, occupation, spoken_languages)" \
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_haver_cert_formula, haver_cert_object.to_tuple())

    def list_all_haverim(self):
        get_all_haverim_formula = "SELECT * FROM Haver"
        self.cursor.execute(get_all_haverim_formula)
        return self.cursor.fetchall()

    def list_all_haverim_cert(self):
        get_all_haverim_cert_formula = "SELECT * FROM HaverCertified"
        self.cursor.execute(get_all_haverim_cert_formula)
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()


def main():
    handler = DatabaseHandler(host='localhost', password='cleo_anthon_123')
    handler.add_haver_to_db(Haver("1234"))
    handler.add_haver_to_db(Haver("1234567"))
    handler.commit()


if __name__ == '__main__':
    main()
