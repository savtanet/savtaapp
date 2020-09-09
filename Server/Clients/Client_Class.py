import threading
from Clients.Connection import send_to_client, receive_from_client
from Text_Parsing.Parse_Text_Params import parse_get_request
from Text_Parsing.Parse_Text_Params import parse_request_words
from Text_Parsing.Parse_Text_Params import convert_haver_to_json
from Text_Parsing.Parse_Text_Params import convert_error_to_json


class client_thread(threading.Thread):
    def __init__(self, client_socket, client_address, db_handler):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.handler = db_handler
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        print('New client thread started successfully. - client {}'.format(self.client_address))

        # Receiving data from the client
        client_http_get_request = receive_from_client(self.client_socket)
        print('Clients request: ', client_http_get_request)
        request, languages, location = parse_get_request(client_http_get_request)

        if request is not None and languages is not None and languages is not [] and location is not None:
            special_requirement = parse_request_words(request)
            print('Clients requirements: {} + {} + {}. - client'.format(location, languages, special_requirement))
            if special_requirement is None:
                haver = self.handler.get_haverim_cert_where_location_langs(location, languages)
            else:
                haver = self.handler.get_haverim_cert_where_location_occupation_langs(location, special_requirement, languages)
            try:
                if haver is []:
                    raise TypeError
                else:
                    haver = haver[0]
                    print("Engine returned {} as the most suitable haver. - client".format(haver))
                    json_obj = convert_haver_to_json(haver)
                    send_to_client(json_obj, self.client_socket)
                    print("Client {} message sent successfully. - client".format(self.client_address))

            except IndexError:
                json_obj = {'Error': 'no suitable haver was found'}
                send_to_client(convert_error_to_json(json_obj), self.client_socket)
                print("No suitable haver was found. - client")

        else:
            print('Client {} has sent an invalid request. - client'.format(self.client_address))

        print("Closing client's {} socket. - client".format(self.client_address))

        # Closing the socket
        self.client_socket.close()
        return
