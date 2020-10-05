import pycurl
import certifi
from io import BytesIO
from urllib.parse import unquote


def get_posts_curl(nodes=['posts'], fields=[['message', 'from']], token_file='Facebook/token.txt'):
    """
    Function:
        This function will get the nodes, fields and token, construct a curl request and handle the curl session.
    Args:
        nodes: Name of nodes. | type: [str,]
        fields: Names of fields for the nodes. | type: [[str,], [str,]]
        *** The number of nodes needs to match the number items in fields.***
        token_file : The path to the file (reletive or absulot). | type: str
    Return:
        String that represents a json object, containing the response from fb. | type: str
    """
    curl = pycurl.Curl()
    response = BytesIO()
    token = get_token_from_file(token_file)

    # constructing request.
    url = parse_facebook_url_request(nodes, fields, token)
    url = convert_to_curl(url)
    url = unquote(url)

    print("---URL---: " + url)

    # curl session and settings.
    curl.setopt(curl.CAINFO, certifi.where())
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEDATA, response)
    curl.perform()
    curl.close()
    return response.getvalue().decode('utf-8')


def convert_to_curl(request):
    """
    Function:
        This function will convert the Graph API request to a curl request.
    Args:
        request: Graph API request. | type: str
    Return:
        valid curl request. | type: str
    """
    # replacing chars that aren't valid in curl requests to their code.
    return request.replace('{', '%7B').replace('}', '%7D').replace(',', '%2C')


def parse_facebook_url_request(nodes, fields, token, version=7.0):
    """
    Function:
        This function will build a request similar to the Graph API Explorer.
    Args:
        nodes: Name of nodes. | type: [str,]
        fields: Names of fields for the nodes. | type: [[str,], [str,]]
        *** The number of nodes needs to match the number items in fields.***
        token : valid token from facebook. | type: str
        version: version of the Graph API. | type: float
    Return:
        request, not valid for curl request, needs convertion. | type: str
    """
    request = 'https://graph.facebook.com/v' + str(version) + '/me?fields='
    # constructing the request using the nodes and fields.
    for node, node_fields in zip(nodes, fields):
        request += node + '{'
        if node_fields:
            for field in node_fields:
                request += field + ','
            request = request[:-1]
        request += '},'
    # adding the access token to the end of the request.
    request = request[:-1] + '&access_token=' + token
    return request


def get_token_from_file(file_name):
    """
    Function:
        This function will get the access token from a given file.
    Args:
        file_name: The path to the file. | type: str.
    Return:
        The access token. | type: str.
    """
    with open(file_name, 'r') as f:
        return f.readline()
