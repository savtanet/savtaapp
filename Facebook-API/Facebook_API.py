import pycurl
from io import BytesIO


'''
Function:
    This function will convert the Graph API request to a curl request.
Args:
    request: Graph API request. | type: str
Return:
    valid curl request. | type: str
'''
def convert_to_curl(request):
    #replacing chars that arn't valid in curl requests to thier code.
    return request.replace('{', '%7B').replace('}', '%7D').replace(',', '%2C')


'''
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
'''
def parse_facebook_url_request(nodes, fields, token, version=7.0):
    request = 'https://graph.facebook.com/v' + str(version) + '/me?fields='
    #constructing the request using the nodes and fields.
    for node, node_fields in zip(nodes, fields):
        request += node + '{'
        if node_fields != []:
            for field in node_fields:
                request += field + ','
            request = request[:-1]
        request += '},'
    #adding the access token to the end of the request.
    request = request[:-1] + '&access_token=' + token
    return request


'''
Function:
    This function will get the access token from a given file.
Args:
    fname: The path to the file (reletive or absulot). | type: str.
Return:
    The access token. | type: str.
'''
def get_token_from_file(fname):
    with open(fname, 'r') as f:
        return f.readline()


'''
Function:
    This function will get the nodes, fields and token, construct a curl request and handle the curl session.
Args:
    nodes: Name of nodes. | type: [str,]
    fields: Names of fields for the nodes. | type: [[str,], [str,]]
    *** The number of nodes needs to match the number items in fields.***
    token_file : The path to the file (reletive or absulot). | type: str
Return:
    String that represents a json object, containing the response from fb. | type: str
'''
def get_posts_curl(nodes=['posts'], fields=[['message','from']], token_file='token.txt'):
    curl = pycurl.Curl()
    response = BytesIO()
    token = get_token_from_file(token_file)

    #constructing request.
    url = parse_facebook_url_request(nodes, fields, token)
    url = convert_to_curl(url)

    #curl session and settings.
    curl.setopt(curl.URL, url)
    curl.setopt(curl.WRITEDATA, response)
    curl.perform()
    curl.close()
    return response.getvalue().decode('utf-8')


if __name__ == "__main__":
    json = get_posts_curl()
    print(json)