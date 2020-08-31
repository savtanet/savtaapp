from Clients.Connection import bind_to_port
from Clients.Server_Class import server_thread
from Facebook.Facebook_Server import facebook_crawler
from Haverim_DB.DB_Handler import database_handler
import time


def main():
    socket = bind_to_port(80)
    print('Binding to port. - main')

    try:
        handler = database_handler(host='192.168.1.26', password='AnthonNaivelt123')

        # 300 is 5 minutes.
        crawler = facebook_crawler(60, handler)

        server = server_thread(socket, handler)

        time.sleep(10)

        # waiting for the server thread to join the main thread.
        print('Main thread is waiting for server thread to join. - main')
        crawler.t.join()
        server.t.join()

    except KeyboardInterrupt:
        socket.close()
        print('Ctrl + C was pressed.')
        return

    except Exception as e:
        socket.close()
        print('Program Terminated Unexpectedly: ' + str(e))
        return

    socket.close()


if __name__ == '__main__':
    main()
