import threading
from Clients.Client_Class import client_thread


class server_thread(threading.Thread):
    def __init__(self, server_socket):
        threading.Thread.__init__(self)
        self.server_socket = server_socket
        self.t = threading.Thread(target=self.execute, args=())
        self.t.daemon = True
        self.t.start()

    def execute(self):
        while True:
            print('Server thread started successfully. - server')
            try:
                print('Server thread is now listening. - server')
                self.server_socket.listen()
                client_socket, client_address = self.server_socket.accept()
                print('Client accepted    ip:{}. - server'.format(client_address))

                client_thread(client_socket, client_address)
                print('Starting new client thread. - server')

            except KeyboardInterrupt:
                raise Exception(KeyboardInterrupt)

            except Exception as e:
                raise Exception(e)
