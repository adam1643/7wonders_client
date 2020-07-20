import json
import socket
import time

SYNC_INTERVAL = 1
request = None
queue = []


def client(game_data):
    while True:
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.connect(('localhost', 15555))
            while True:
                game_data.send_sync()
                time.sleep(SYNC_INTERVAL)
                while len(queue) > 0:
                    req = queue.pop(0)
                    if req is False:
                        print("Quitting application...")
                        server.close()
                        return
                    # print('req', req)
                    if True:
                        server.send(json.dumps(req).encode('utf8'))
                        response = server.recv(1023).decode('utf8')
                        # print("Response", response)
                        game_data.parse_response(response)
        except KeyboardInterrupt:
            server.close()
        except:
            server.close()
            print("No connection")
        for req in queue:
            if req is False:
                print("Quitting application...")
                return
        time.sleep(5)
