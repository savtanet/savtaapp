class Haver:
    def __init__(self, name, facebook_id):
        self.facebook_profile_name = name
        self.facebook_profile_id = facebook_id

    def __str__(self):
        return "User {}.".format(self.facebook_profile_name)

    def to_tuple(self):
        return self.facebook_profile_name, self.facebook_profile_id


class HaverCertified:
    def __init__(self, name, location, phone, facebook_id, email, occupation, languages):
        self.name = name
        self.location = location
        self.phone = phone
        self.facebook_id = facebook_id
        self.email = email
        self.occupation = occupation
        self.spoken_languages = languages

    def __str__(self):
        return "User: {} [location: {}, phone: {}]".format(self.name, self.location, self.phone)

    def to_tuple(self):
        languages = ""
        for lang in self.spoken_languages:
            languages = languages + lang + '+'
        return self.name, self.location, self.phone, self.facebook_id, self.email, self.occupation, languages[:-1]
