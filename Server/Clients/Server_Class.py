import threading
from Clients.Client_Class import ClientThread


class ServerThread(threading.Thread):
    def __init__(self, server_socket, db_handler):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.handler = db_handler
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        clients = []

        while True:
            try:
                print('Server thread is now listening. - server')
                self.server_socket.listen()
                client_socket, client_address = self.server_socket.accept()

                clients.append(ClientThread(client_socket=client_socket,
                                            client_address=client_address,
                                            db_handler=self.handler))

            except KeyboardInterrupt:
                raise Exception(KeyboardInterrupt)
