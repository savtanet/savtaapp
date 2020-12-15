from Clients.Connection import bind_to_port
from Clients.Server_Class import ServerThread
from Haverim_DB.DB_Handler import DatabaseHandler


def main():
    socket = bind_to_port(80)
    print('Binding to port. - main')

    try:
        handler = DatabaseHandler(host='localhost', user='root', password='cleo_anthon_123')

        server = ServerThread(socket, handler)
        server.t.join()

    except KeyboardInterrupt:
        print('Ctrl + C was pressed.')

    except Exception as e:
        print('Program Terminated Unexpectedly: ' + str(e))

    socket.close()
    return 


if __name__ == '__main__':
    main()
