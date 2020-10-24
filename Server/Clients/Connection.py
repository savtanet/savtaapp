import socket

def bind_to_port(port):
    try:
        # Create a TCP/IP socket
        listening_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Binding to port
        server_address = ('', port)
        listening_sock.bind(server_address)
    except Exception as e:
        print("Error: ", e)
        return None

    return listening_sock


def receive_from_client(client_soc):
    try:
        return client_soc.recv(1024).decode()
    except Exception as e:
        print("Exception: " + str(e))
        return None


def send_to_client(msg, client_soc):
    client_soc.sendall(msg.encode())
