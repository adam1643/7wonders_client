from http_client import queue
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
        self.first_get = True

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
            elif data.get('type') == 'first_get_data':
                self.parse_first_game_data(data)
                self.gui.wonder_signal.emit(data.get('wonder'))
                self.gui.game_update_signal.emit(1)
            elif data.get('type') == 'get_move':
                print("Get move", data)
                self.parse_get_move_response(data)
            elif data.get('type') == 'sync':
                self.parse_sync_response(data)
            elif data.get('type') == 'build':
                print("Build response", data)
                status = data.get('status')
                if status is False:
                    self.gui.error_signal.emit(10)
            elif data.get('type') == 'card_details':
                print("Card details", data)
                self.parse_card_details(data)
            elif data.get('type') == 'wonder_details':
                print("Wonder details", data)
                self.parse_wonder_details(data)
            elif data.get('type') == 'end_age':
                self.parse_end_age(data)
            elif data.get('type') == 'end_game':
                self.parse_end_game(data)
            elif data.get('type') == 'get_discarded':
                discarded = data.get('discarded')
                self.gui.show_discarded_signal.emit(discarded)
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

    def parse_first_game_data(self, data):
        self.parse_game_data(data)
        built = data.get('built_cards')
        left = data.get('left_built_cards')
        right = data.get('right_built_cards')
        self.gui.first_game_update_signal.emit(built, left, right)

    def parse_sync_response(self, data):
        login = data.get('id')
        if login != self.login:
            return

        ready = data.get('players_ready')
        player = data.get('player_waiting')
        left = data.get('left_waiting')
        right = data.get('right_waiting')
        self.gui.queue_text.emit([ready, player, left, right])

        end_age = data.get('end_age')
        new_move = data.get('move_ready')
        if end_age is True:
            self.send_end_age_req()
        if new_move is True:
            print("MOVE MOVE MOVE")
            self.send_get_move_req()

        update = data.get('update')
        if update is True:
            self.send_game_data_req()

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
        money, military = data.get('money'), data.get('military')
        wins, loses = data.get('wins'), data.get('loses')
        discarded = data.get('discarded')
        if discarded is True:
            self.gui.show_discarded_signal.emit(1)
        else:
            self.gui.new_move_signal.emit(player_build, left_build, right_build, [money, military, wins, loses])
        print("Get move", data)

    def parse_end_age(self, data):
        player = data.get('player_battle')
        left = data.get('left_battle')
        right = data.get('right_battle')
        self.gui.end_age_signal.emit(player, left, right)

    def parse_end_game(self, data):
        players = data.get('players')
        battles = data.get('battles')
        money = data.get('money')
        blue, wonder = data.get('blue'), data.get('wonder')
        yellow, green, purple = data.get('yellow'), data.get('green'), data.get('purple')
        self.gui.end_game_signal.emit(players, battles, money, blue, wonder, yellow, green, purple)

    def parse_card_details(self, data):
        res = data.get('resources_needed')
        availability = data.get('resources_available')
        upgrade = data.get('upgrade')
        self.gui.card_details_signal.emit(res, availability, upgrade)

    def parse_wonder_details(self, data):
        res = data.get('resources_needed')
        avail = data.get('resources_available')
        upgrade = False
        self.gui.card_details_signal.emit(res, avail, upgrade)

    def send_login(self, login):
        data = {'type': 'login', 'id': login}
        self.login = login
        queue.append(data)

    def send_sync(self):
        data = {'type': 'sync', 'id': self.login}
        queue.append(data)

    def send_game_data_req(self):
        if self.first_get is True:
            data = {'type': 'first_get_data', 'id': self.login}
            self.first_get = False
        else:
            data = {'type': 'get_data', 'id': self.login}
        queue.append(data)

    def send_build_req(self, index, chosen, discard=False, wonder=False):
        data = {'type': 'build', 'id': self.login, 'building': index, 'chosen': chosen, 'discard': discard, 'wonder': wonder}
        queue.append(data)

    def send_get_move_req(self):
        data = {'id': self.login, 'type': 'get_move'}
        queue.append(data)

    def send_card_details_req(self, index):
        data = {'id': self.login, 'type': 'card_details', 'card_id': index}
        queue.append(data)

    def get_discarded_req(self):
        data = {'id': self.login, 'type': 'get_discarded'}
        queue.append(data)

    def send_wonder_details_req(self, index):
        data = {'id': self.login, 'type': 'wonder_details', 'wonder_id': index}
        queue.append(data)

    def send_build_discarded(self, index):
        data = {'id': self.login, 'type': 'build_discarded', 'card_id': index}
        queue.append(data)

    def send_end_age_req(self):
        data = {'id': self.login, 'type': 'end_age'}
        queue.append(data)

    def send_end_game_req(self):
        data = {'id': self.login, 'type': 'end_game'}
        queue.append(data)
