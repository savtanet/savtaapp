class haver:
    def __init__(self, name, location, phone):
        self.name = name
        self.city = location
        self.phone = phone
        self.facebook_id = ''

    def __str__(self):
        return 'Name: ' + self.name + ' Location: ' + self.city + '. (Haver)'

    def to_tuple(self):
        return self.name, self.city, self.phone, self.facebook_id


class haver_cert:
    def __init__(self, name, location, phone, facebook_id, email, occupation, langs):
        self.name = name
        self.city = location
        self.phone = phone
        self.facebook_id = facebook_id
        self.email = email
        self.occupation = occupation
        self.langs = langs

    def __str__(self):
        return 'Name: ' + self.name + ' Location: ' + self.city + ' Job: ' + self.occupation + '. (Cert)'

    def to_tuple(self):
        languages = ""
        for lang in self.langs:
            languages = languages + lang + ','

        return self.name, self.city, self.phone, self.facebook_id, self.email, self.occupation, languages[:-1]
