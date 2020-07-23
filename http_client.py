import http.client
import json
import time

HOST = 'localhost'
PORT = 1643
SYNC_INTERVAL = 1
RETRY_INTERVAL = 5
HEADERS = {'Content-type': 'application/json'}
queue = []


def client(game_data):
    while True:
        try:
            conn = http.client.HTTPConnection(f'{HOST}:{PORT}')
            while True:
                game_data.send_sync()
                time.sleep(SYNC_INTERVAL)
                while len(queue) > 0:
                    req = queue.pop(0)
                    if req is False:
                        print("Quitting application...")
                        conn.close()
                        return
                    conn.request('POST', '/', json.dumps(req), HEADERS)
                    response = conn.getresponse().read().decode()
                    game_data.parse_response(response)
        except KeyboardInterrupt:
            conn.close()
        # except:
            conn.close()
            print("No connection")
        for req in queue:
            if req is False:
                print("Quitting application...")
                return
        time.sleep(RETRY_INTERVAL)
