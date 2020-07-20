from client import queue
import json


class GameData:
    def __init__(self):
        self.login = 'a'
        self.queue = 0

        self.gui = None

        self.cards = []
        self.money = 0
        self.vp = 0
        self.military = 0

        self.wonder = 0

        self.left_neighbor = []
        self.right_neighbor = []

        self.ready = 0

        self.top_data = None

    def set_gui(self, gui):
        self.gui = gui

    def parse_response(self, data):
        data = json.loads(data)

        if 'error' in data.keys():
            print("BAD", data)
            UserWarning("Bad response")

        if 'type' in data.keys():
            if data.get('type') == 'get_data':
                print(data.get('cards'), data.get('wonder'))
                self.parse_game_data(data)
                self.gui.wonder_signal.emit(data.get('wonder'))
                self.gui.game_update_signal.emit(1)
            elif data.get('type') == 'get_move':
                print("Get move", data)
                self.parse_get_move_response(data)
            elif data.get('type') == 'sync':
                self.parse_sync_response(data)
            elif data.get('type') == 'build':
                print("Build response", data)
            elif data.get('type') == 'card_details':
                print("Card details", data)
                self.parse_card_details(data)
            else:
                print("Bad response type", data)
        else:
            print("Bad response", data)

    def parse_game_data(self, data):
        self.money = data.get('money')[0]
        self.vp = data.get('vp')
        self.military = data.get('military')
        self.cards = data.get('cards')

        self.left_neighbor = data.get('left_neighbor')
        self.right_neighbor = data.get('right_neighbor')

        self.top_data = [data.get('money'), data.get('military'), data.get('wins'), data.get('loses')]

    def parse_sync_response(self, data):
        login = data.get('id')
        if login != self.login:
            return

        ready = data.get('players_ready')
        left = data.get('left_waiting')
        right = data.get('right_waiting')
        self.gui.queue_text.emit([ready, left, right])

        new_move = data.get('move_ready')
        if new_move is True:
            print("MOVE MOVE MOVE")
            self.send_get_move_req()

        update = data.get('update')
        if update is True:
            self.send_game_data_req()

        # print(data)

        # players_queue = data.get('queue')
        # print('Players in queue: ', players_queue)
        # self.queue = players_queue
        #
        # print("Queue", self.queue)

        # self.gui.queue_text.emit(self.queue)
        # self.gui.wonder_signal.emit(self.queue)

    def parse_game_data_resposne(self, data):
        data = json.loads(data)
        login = data.get('id')
        if login != self.login:
            return

        cards = data.get('cards')
        print(cards)

    def parse_get_move_response(self, data):
        player_build = data.get('player_built')
        left_build = data.get('left_neighbor_built')
        right_build = data.get('right_neighbor_built')
        delta = data.get('player_money_delta')
        self.gui.new_move_signal.emit(player_build, left_build, right_build, [0, delta, 0])
        print("Get move", data)

    def parse_card_details(self, data):
        res = data.get('resources_needed')
        availability = data.get('resources_available')
        self.gui.card_details_signal.emit(res, availability)

    def send_login(self, login):
        data = {'type': 'login', 'id': login}
        self.login = login
        queue.append(data)

    def send_sync(self):
        data = {'type': 'sync', 'id': self.login}
        queue.append(data)

    def send_game_data_req(self):
        data = {'type': 'get_data', 'id': self.login}
        queue.append(data)

    def send_build_req(self, index, chosen, discard=False):
        data = {'type': 'build', 'id': self.login, 'building': index, 'chosen': chosen, 'discard': discard}
        queue.append(data)

    def send_get_move_req(self):
        data = {'id': self.login, 'type': 'get_move'}
        queue.append(data)

    def send_card_details_req(self, index):
        data = {'id': self.login, 'type': 'card_details', 'card_id': index}
        queue.append(data)
