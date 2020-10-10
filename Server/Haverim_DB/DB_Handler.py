import mysql.connector


class database_handler:
    def __init__(self, password=None, host='localhost', user='AnthonGar', database='development'):
        if password is None:
            password = input("Please enter your MySQL user password: ")
        print('Attempting to connect to MySQL data base. - db handler')
        self.db = mysql.connector.connect(host=host, user=user, password=password)
        self.cursor = self.db.cursor()
        self.cursor.execute('USE ' + database)
        print('Connected to MySQL data base. - db handler')

    def add_haver_to_db(self, haver_object):
        insert_haver_formula = "INSERT INTO haverim" \
                               " (name, location, phone, facebook_id)" \
                               " VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(insert_haver_formula, haver_object.to_tuple())
        except mysql.connector.errors.IntegrityError:
            print("Duplicate")
            pass

    def add_haver_cert_to_db(self, haver_cert_object):
        insert_haver_cert_formula = "INSERT INTO haverim_cert" \
                                    " (name, location, phone, facebook_id, email, occupation, langs)" \
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.cursor.execute(insert_haver_cert_formula, haver_cert_object.to_tuple())

    def list_all_haverim(self):
        get_all_haverim_formula = "SELECT * FROM haverim"
        self.cursor.execute(get_all_haverim_formula)
        return self.cursor.fetchall()

    def list_all_haverim_cert(self):
        get_all_haverim_cert_formula = "SELECT * FROM haverim_cert"
        self.cursor.execute(get_all_haverim_cert_formula)
        return self.cursor.fetchall()

    def get_haverim_cert_where_location_occupation_langs(self, location, occupation, langs):
        params = [location, occupation]
        languages = ""
        get_cert_formula = "SELECT * FROM haverim_cert WHERE location = %s AND occupation = %s AND langs LIKE CONCAT('%',%s,'%')"

        for lang in langs:
            languages = languages + lang + '+'
        params.append(languages[:-1])

        self.cursor.execute(get_cert_formula, tuple(params))
        return self.cursor.fetchall()

    def get_haverim_cert_where_location_langs(self, location, langs):
        params = [location]
        languages = ''
        get_cert_formula = "SELECT * FROM haverim_cert WHERE location = %s AND langs LIKE CONCAT('%',%s,'%')"

        for lang in langs:
            languages = languages + lang + '+'
        params.append(languages[:-1])

        self.cursor.execute(get_cert_formula, tuple(params))
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()


def main():
    handler = database_handler(host='localhost', password='AnthonNaivelt123')
    res = handler.get_haverim_cert_where_location_langs(location="Ashdod", langs="he")
    print(res)


if __name__ == '__main__':
    main()
