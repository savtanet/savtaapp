import threading
from Clients.Connection import send_to_client, receive_from_client
from Text_Parsing.Parse_Text_Params import add_html_headers
from Text_Parsing.Parse_Text_Params import convert_error_to_json
from Text_Parsing.Parse_Text_Params import emergency_contact_json
from Text_Parsing.Parse_Text_Params import convert_tuple_to_json
from Text_Parsing.Parse_Text_Params import parse_get_request
from Text_Parsing.NPL_Engine import determine_emergency_query, EMERGENCY_THRESHOLD


class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address, db_handler):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.handler = db_handler
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        client_http_get_request = receive_from_client(self.client_socket)
        if client_http_get_request is not None:
            request, location, language = parse_get_request(client_http_get_request)

            if request is not None and language is not None and location is not None:
                emergency = False
                emergency_request_score = determine_emergency_query(request)
                if emergency_request_score > EMERGENCY_THRESHOLD:
                    emergency = True

                return_list = convert_tuple_to_json(self.handler.get_haver_near_you(location, language))
                if not return_list:
                    error_object = {'Error': 'no suitable haver was found'}
                    send_to_client(convert_error_to_json(error_object), self.client_socket)
                    self.client_socket.close()
                    return

                if emergency:
                    return_list = emergency_contact_json() + return_list

                http_response = add_html_headers(str(return_list))
                send_to_client(http_response, self.client_socket)
                self.client_socket.close()
                return
        else:
            self.client_socket.close()
            return
