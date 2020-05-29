import threading
import get_query
EXIT = "exit"

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.clientAddress = clientAddress
        self.clientSock = clientSocket
        print("New connection added: ", self.clientAddress)

    def run(self):

        #while True:
        # Receiving data from the client
        client_msg = self.clientSock.recv(1024)
        client_msg = client_msg.decode()

        if client_msg == EXIT:
            pass
            #break

        msgToCllient = get_query.clientMsgHandler(client_msg)

        # Sending data back
        self.clientSock.sendall(msgToCllient.encode())


        # Closing the conversation socket
        self.clientSock.close()


        print("Client at ", self.clientAddress, " disconnected...")
