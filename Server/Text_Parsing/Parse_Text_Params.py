from Haverim_DB.haverim_class import haver


def parse_post_class_haver(text, cities=[], names=[]):
    """
    Description: This function will try to parse simple text into a 'haver' class object. I will search the given text for a location in Israel,
                 a name, and a string of numbers that might be the phone number of the same person.
    Input: text - String - the text that is needed to be parsed.
           cities - List<String> - list of names of cities in Israel. If left empty, the function will read the locations for a txt file.
           names - List<String> - list of names. If left empty, the function will read the names form a txt file.
    Output: If the parsing was successful, 'haver' class object, else, None.
    """
    if not cities:
        with open('Text_Parsing/Cities_List.txt', 'r') as f:
            while True:
                city = f.readline().replace('\n', '')
                if city == '':
                    break
                else:
                    cities.append(city)

    if not names:
        with open('Text_Parsing/Names_List', 'r') as f:
            while True:
                name = f.readline().replace('\n', '')
                if name == '':
                    break
                else:
                    names.append(name)

    phone_number = ''
    location = ''
    identity = ''
    numeric_substrings = find_number_substrings(text)

    for city in cities:
        if city in text:
            location = city
            break

    for name in names:
        if name in text:
            identity = name
            break

    for number in numeric_substrings:
        if is_phone(number):
            phone_number = number
            break

    if location == '' or identity == '' or phone_number == '':
        return None
    else:
        return haver(identity, location, phone_number)


def is_age(number):
    if 10 <= int(number) <= 99:
        return True
    else:
        return False


def is_phone(number):
    if len(number) == 10:
        return True
    else:
        return False


def find_number_substrings(text):
    return [str(s) for s in text.split() if s.isdigit()]


def parse_get_request(get_request):
    try:
        params = list(filter(None, get_request.split('0')[1].split('/')))
        return params[0], params[1:-1:1], params[-1]

    except IndexError:
        return None, None, None


def parse_client_request(client_request):
    pass