from Clients.Connection import bind_to_port
from Clients.Server_Class import server_thread
from Facebook.Facebook_Server import facebook_crawler
import time


def main():
    socket = bind_to_port(80)
    print('Binding to port. - main')

    try:
        # 300 is 5 minutes.
        crawler = facebook_crawler(60)

        server = server_thread(socket)

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
