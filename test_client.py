import json
import socket


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect(('localhost', 15555))

# req = {'id': 'c', 'type': 'get_data'}
# server.send(json.dumps(req).encode('utf8'))
# response = server.recv(255).decode('utf8')
# data = json.loads(response)
# cards = data.get('cards')
# card = cards[0]
# req = {'id': 'c', 'type': 'build', 'building': card}
# server.send(json.dumps(req).encode('utf8'))
# response = server.recv(255).decode('utf8')
# print("Response", response)
#
# req = {'id': 'b', 'type': 'get_data'}
# server.send(json.dumps(req).encode('utf8'))
# response = server.recv(255).decode('utf8')
# data = json.loads(response)
# cards = data.get('cards')
# card = cards[0]
# req = {'id': 'b', 'type': 'build', 'building': card}
# server.send(json.dumps(req).encode('utf8'))
# response = server.recv(255).decode('utf8')
# print("Response", response)


req = {'id': 'b', 'type': 'get_move'}
server.send(json.dumps(req).encode('utf8'))
response = server.recv(255).decode('utf8')
print("Response", response)

req = {'id': 'c', 'type': 'get_move'}
server.send(json.dumps(req).encode('utf8'))
response = server.recv(255).decode('utf8')
print("Response", response)



#
# req = {'id': 'c', 'type': 'get_data'}
# server.send(json.dumps(req).encode('utf8'))
# response = server.recv(255).decode('utf8')
# print("Response", response)


server.close()
