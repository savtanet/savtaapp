import json
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
        with open('Text_Parsing/Names_List.txt', 'r') as f:
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
        lines = get_request.split('\n')
        for line in lines:
            if "GET" in line:
                break

        # params: [junk, request, langs, location + junk]
        params = line.split('/')
        # removing headings: [request, langs, location + junk]
        params = params[1:-1]

        request, langs, location = params

        # clearing location param
        location = location.split(" ")
        location = location[0]

        # clearing request:
        request = request.replace("+", " ")

        # parsing languages:
        langs = langs.split("+")

        return request, langs, location

    except IndexError:
        return None, None, None

    except ValueError:
        return None, None, None


def parse_request_words(client_request):
    key_list = []
    value_list = []

    with open("Text_Parsing/Requests.txt") as file:
        while True:
            line = file.readline().replace('\n', '').split(':')
            if line != ['']:
                try:
                    key_list.append(line[0])
                    value_list.append(line[1])
                except IndexError:
                    print('-> ' + str(line) + ' THIS IS THE ERROR')
            else:
                break

    request_dict = dict(zip(key_list, value_list))

    for word in client_request.split(" "):
        if word in request_dict.keys():
            special_requirement = request_dict[word]
            if special_requirement == "general":
                special_requirement = None
            break
        else:
            special_requirement = None

    return special_requirement


def convert_haver_to_json(suitable_haver):
    json_haver = {
        'Name': suitable_haver[0],
        'Phone': suitable_haver[2],
        'Occupation': suitable_haver[5],
        'Languages': suitable_haver[6]
    }
    return json.dumps(json_haver)


def convert_error_to_json(msg):
    return json.dumps(msg)


def add_html_headers(msg):
    res = "HTTP/1.1 200 OK\r\n"
    res += "Content-Type: application/json; charset-utf-8\r\n"
    res += "Connection: Closed\r\n"
    res += "\r\n"
    res += msg + "\r\n"
    res += "\r\n"


def main():
    special = parse_request_words("i need help to find remote")
    print(special)


if __name__ == '__main__':
    main()
