import socket
import _thread
class Client():
    def __init__(self, name, server_ip="localhost", port=1234):
        self.HEADER_LEN = 5
        self.name = name
        self.sock = socket.socket()
        self.sock.connect((server_ip, port))
        print(f"Connected to {server_ip}:{port}")
        self.send_data(self.sock, self.name)
        self.name = self.recv_data()
        self.game_state = GameState()
        self.choice = None
        print(self.name)
        # run logic 
        # Done on a thread interfaced with global variables (very hacky but works)
        _thread.start_new_thread(self.connection_logic, ())
       

    def connection_logic(self):
        """Recieves and interperates information from the server"""
        while True:
            msg = self.recv_data()
            packet_state = self.game_state.interperate_state(msg)
            if packet_state == "state":
                print(self.game_state.return_full_state())
                if self.game_state.curr_name == self.name:
                    # Players turn buffer until choice made
                    while self.choice == None:
                        self.send_data(self.sock, "...")
                    self.send_data(self.sock, self.choice)
                    self.choice = None
            else:
                print(msg)


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

    def send_data(self, target_sock, msg):
        """Using fixed length headers to form a buffer so client knows
        how long packets are"""
        msg_len = len(msg)
        # eg b'10   HelloWorld' note that header is exactly 5 chars long
        target_sock.send(bytes(f"{msg_len:<{self.HEADER_LEN}}{msg}", "utf-8"))
        return(True)


class GameState():
    """Used as a struct to store game state data """
    def __init__(self):
        # Vars from state packet
        self.round = None
        self.cards_left = None
        self.cards_per_round = None
        self.curr_card = None
        self.curr_stack = None
        self.curr_name = None
        self.curr_bank = None
        # Vars from player list protocol
        self.connected_players = []
        self.max_players = 2
        self.has_started = False

    def interperate_state(self, raw_packet):
        """state:round,cards_left,cardsperround,curr_card,curr_stack,curr_name,curr_bank"""
        packet_type = raw_packet.split(":")
        if packet_type[0] == "state":
            data = packet_type[1].split(",")
            try:
                self.round =           data[0]
                self.cards_left =      data[1]
                self.cards_per_round = data[2]
                self.curr_card =       data[3]
                self.curr_stack =      data[4]
                self.curr_name =       data[5]
                self.curr_bank =       data[6]
                return('state')
            except IndexError:
                print("Invalid state packet")
                return(False)

        if "players" in packet_type[0]:
            self.max_players = packet_type[0].split("/")[1]
            self.connected_players = packet_type[1].split(" ")
            return('lobby')
        
        elif 'starting game' == raw_packet:
            self.has_started = True
            return('start')
        return(False)

    def return_full_state(self):

        """returns entire state packet as a tuple"""
        return(self.round, self.cards_left, self.cards_per_round,\
            self.curr_card,self.curr_stack, self.curr_name, self.curr_bank)

    

if __name__ == "__main__":
    client = Client("Bob")
