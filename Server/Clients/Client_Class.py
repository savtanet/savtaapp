import threading
from Clients.Connection import send_to_client, receive_from_client
from Text_Parsing.Parse_Text_Params import parse_get_request


class client_thread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        print('New client thread started successfully. - client {}'.format(self.client_address))

        # Receiving data from the client
        client_http_get_request = receive_from_client(self.client_socket)
        request, languages, location = parse_get_request(client_http_get_request)

        if request is not None and languages is not None and languages is not [] and location is not None:
            pass
        else:
            print('Client {} has sent an invalid request. - client'.format(self.client_address))

        print("Closing client's {} socket. - client".format(self.client_address))

        # Closing the socket
        self.client_socket.close()
        return

    def handle_client_request(self, request, languages, location):
        return
