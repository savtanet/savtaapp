import socket

from Posts_Parser import FacebookManager

LISTEN_PORT = 2512
from ClientThread import ClientThread

def start_connection():
    """
	The function will start a TCP connection
    """
    try:
        # Create a TCP/IP socket
        listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binding to local port 2512
        server_address = ('', LISTEN_PORT)
        listening_sock.bind(server_address)
    except Exception as e:
        print("Error: ", e)

    return listening_sock


def startServer():

    facebookManager = FacebookManager()
    facebookManager.start()

    #starting TCP connection
    listening_sock = start_connection()

    while True:
        # Listen for incoming connections
        listening_sock.listen(1)

        # Create a new conversation socket
        client_soc, client_address = listening_sock.accept()

        # New client thraed
        newClientThread = ClientThread(client_address, client_soc)
        newClientThread.start()

    # Closing the listening socket
    listening_sock.close()

def main():
    startServer()

if __name__ == "__main__":
    main()
