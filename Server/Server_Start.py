from Clients.Connection import bind_to_port
from Clients.Server_Class import server_thread
from Facebook.Facebook_Server import facebook_crawler
from Haverim_DB.DB_Handler import database_handler


def main():
    socket = bind_to_port(80)
    print('Binding to port. - main')

    try:
        handler = database_handler(host='localhost', password='AnthonNaivelt123')

        # 300 is 5 minutes.
        crawler = facebook_crawler(60, handler)

        server = server_thread(socket, handler)

        # time.sleep(10)

        # waiting for the server thread to join the main thread.
        print('Main thread is waiting for server thread to join. - main')
        crawler.t.join()
        server.t.join()

    except KeyboardInterrupt:
        print('Ctrl + C was pressed.')

    except Exception as e:
        print('Program Terminated Unexpectedly: ' + str(e))

    socket.close()
    return 


if __name__ == '__main__':
    main()
