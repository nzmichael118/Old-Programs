"""Hosts the game logic and manages clients"""
"""Lobby system gets players, then sends packet telling all players
that game is full and starting
then the actual game logic sends a ping to playing player telling them 
they are playing then awaits its response after which it processes logic
updates everyone on game states then repeats"""

import datetime
import socket
import highlowlogic

class GameServer():
    """ 
    States:
                                                   V--------------------------------------------|
    Get players -> Broadcast start -> MSG starting player -> wait for choice -> broadcast state ^
    """

    def __init__(self, max_players=3):
        PORT = 1234
        self.HEADER_LEN = 5  # max 99999 bytes in a packet more than enough
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.sock.bind((socket.gethostname(), 1234))
        self.sock.bind(("localhost", PORT))
        self.sock.listen(8)  # amount of requests can handle at once
        self.max_players = max_players

        # Stages of Game Server
        self.clients = self.lobby(self.max_players)
        self.names = []
        for client in self.clients:
            self.names.append(client.name)

        self.start_game()

    def start_game(self):
        """Runs main game loop"""
        self.broadcast_all(self.clients, "starting game")
        self.game = highlowlogic.Game(self.names)

        while self.game.get_round() > 0:
            # Run loop until game is over
            # Just broadcasts states to all players
            # and listens in for current players packets
            msg = self.game.get_entire_state()
            # msg:
            # 'state:round,cards_left,cardsperround,curr_card,curr_stack,curr_name,curr_bank'
            decoded = msg.split(",")
            curr_name = decoded[5]
            print(msg)
            self.broadcast_all(self.clients, msg)
            
            # wait curr playing response
            choice = "..."
            for client in self.clients:
                if client.name == curr_name:
                    while choice == "...":
                        choice = client.recv_data()
                    
            print(curr_name)
            self.game.player_choice(choice, curr_name)

        

    def lobby(self, max_players):
        """Recieves inbound socket connections and when all clients are joined
        sends ping to each player to let know game starts."""
        clients = []
        # name_list exists to prevent duplicate names
        name_list = []
        while True:
            self.sock.listen()
            c, addr = self.sock.accept()
            print(f"Connection from: {addr}, {datetime.datetime.now()}")
            clients.append(Client(c, name_list))
            name_list.append(clients[-1].name)
            self.send_player_names(clients, max_players)

            if len(clients) == max_players:
                return(clients)

    def broadcast_all(self, players, msg):
        """Send msg to all players"""
        for player in players:
            player.send_data(msg)
        return(True)

    def send_player_names(self, players, max_players):
        """Dedicated to the player name protocol sent after each player join
        send"players/8:name1 name2 name3" Seperated by ' '(space)"""
        name_list = ""
        for player in players:
            name_list = f"{name_list} {player.name}"
        msg = f"players/{max_players}:{name_list}"
        # Send package to all players
        self.broadcast_all(players, msg)

        return(True)


class Client():

    def __init__(self, sock, taken_names):
        self.HEADER_LEN = 5
        """Socket.socket(), string list[]"""
        self.sock = sock
        self.name = "Placeholder"
        self.set_name(taken_names)

    def set_name(self, taken_names):
        """Cannot setup name until class is instansiated
        Takes in client package then sends name sent to confirm9"""
        chosen_name = self.recv_data().replace(" ", "").replace(",", "")
        if chosen_name not in taken_names:
            self.name = chosen_name
            self.send_data(self.name)
        else:
            # if name such as 'bob' is taken then will set name to 'bob1'
            # or 'bob2' ect..
            i = 1
            temp_chosen = f"{chosen_name}{i}"
            while temp_chosen in taken_names:
                i += 1
                temp_chosen = f"{chosen_name}{i}"

            self.name = temp_chosen
            self.send_data(self.name)

    def send_data(self, msg):
        """Using fixed length headers to form a buffer so client knows
        how long packets are"""
        msg_len = len(msg)
        # eg b'10   HelloWorld' note that header is exactly 5 chars long
        self.sock.send(bytes(f"{msg_len:<{self.HEADER_LEN}}{msg}", "utf-8"))
        return(True)

    def recv_data(self):
        """Recieves header buffer then recieves msg"""
        header = self.sock.recv(self.HEADER_LEN)
        try:
            msg_len = int(header.decode("utf-8"))
        except TypeError:
            return("Error Invalid Header")

        msg = self.sock.recv(msg_len)
        msg = msg.decode("utf-8")
        return(msg)


if __name__ == "__main__":
    server = GameServer(3)
