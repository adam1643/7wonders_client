import json
import socket
import time

SYNC_INTERVAL = 3
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
                    # print('req', req)
                    if True:
                        server.send(json.dumps(req).encode('utf8'))
                        response = server.recv(255).decode('utf8')
                        # print("Response", response)
                        game_data.parse_response(response)
        except KeyboardInterrupt:
            server.close()
        except:
            server.close()
            print("No connection")
        time.sleep(5)
