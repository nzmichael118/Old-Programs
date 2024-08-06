"""Sets up functions and classes to run the highlow game logic"""

import cards


class Game():
    """"Runs main game logic"""

    def __init__(self, players, rounds=10,cards_per_round=10, deck_size=1):
        """"array[string] players, int rounds, int decksize"""
        self.deck = cards.Deck(deck_size)
        self.rounds = rounds
        self.cards_per_round = cards_per_round
        self.players = []
        for name in players:
            self.players.append(Players(name))

        self.swap_cost = 50
        self.stack_size = 0
        self.card_reward = 100
        self.curr_cards_left = self.cards_per_round
        self.curr_player_index = 0
        self.curr_player_guesses = 0

        # First drawn card of game
        self.curr_card = self.draw_new_card()

    def get_entire_state(self):
        """Returns all information for server as a string
        state:round,cards_left,cardsperround,curr_card,curr_stack,curr_name,curr_bank"""
        # Todo make this line shorter v
        return(f"state:{self.rounds},{self.curr_cards_left},{self.cards_per_round},{self.get_current_card()},{self.stack_size},{self.get_current_player().name},{self.get_current_player().bank}")

    def get_round(self):
        """returns rounds remaining"""
        return(self.rounds)

    def get_current_player(self):
        """Returns class instance of current player"""
        return(self.players[self.curr_player_index])

    def get_current_card(self):
        return(self.curr_card)

    def get_winner(self):
        """returns array of players in order of highest bank [0] being highest"""
        # sort based on bank value
        scoreboard = sorted(self.players, key=lambda x: x.bank, reverse=True)
        
        return(scoreboard)
        
    def draw_new_card(self):
        """Draws card and returns it (removes the tuple)"""
        self.curr_cards_left -= 1
        if self.curr_cards_left <= 0:
            self.rounds -= 1
            self.curr_cards_left = self.cards_per_round
        output = self.deck.draw_card()
        return(output[0])

    def next_player(self):
        self.curr_player_guesses = 0
        if self.curr_player_index < len(self.players) - 1:
            self.curr_player_index += 1
        else:
            self.curr_player_index = 0
            #self.rounds -= 1
    # Player actions


    def player_choice(self, choice, player_name):
        """Takes in a players choice to determine output, 
        takes player_name as a semi-protection to prevent
        a different player for making another players turn

        returns: a bool for whether player is still in game
        truth table:
        correct High Low: True
        bank: False, (True if not possible)
        swap: True

        Throws error if incorrect 
        """
        if self.get_current_player().name == player_name:
            # Choice input sanitised in interface not here
            # if only python < 3.10 had switch cases :/
            if choice == "bank":
                if self.curr_player_guesses >= 1:
                    # Only can bank if made correct guess
                    self.get_current_player().deposit(
                        self.stack_size * self.card_reward)
                    
                    self.stack_size = 0
                    self.next_player()

                    return(False)
                else:
                    # Failed bank
                    return(True)
            elif choice == "swap":
                # Swaps cost money
                if self.get_current_player().bank >= self.swap_cost:
                    self.curr_card = self.draw_new_card()
                    self.get_current_player().withdraw(self.swap_cost)
                return(True)

            else:
                # Either invalid input or guessing higher or lower
                new_card = self.draw_new_card()
                # Use diff instead of checking high low saves ~3 if statements
                # of edge cases (same as)
                card_diff = new_card.value - self.curr_card.value
                #   +      =  8   - 4
                if choice == "higher":

                    self.curr_card = new_card
                    self.stack_size += 1
                    if card_diff > 0:
                        # Correct guess
                        self.curr_player_guesses += 1
                        return(True)
                    else:
                        self.next_player()
                        return(False)

                elif choice == "lower":
                    self.curr_card = new_card
                    self.stack_size += 1
                    if card_diff < 0:
                        # Correct guess
                        self.curr_player_guesses += 1
                        return(True)
                    else:
                        self.next_player()
                        return(False)

                else:
                    # Incorrect choice option
                    raise ValueError(f'innapropriate choice value {choice}')
        else:
            # Incorrect player name
            raise ValueError(f'innapropriate username value {player_name}')


class Players():
    """Stores data about players"""

    def __init__(self, name):
        self.name = name
        self.bank = 500  # Init money

    def withdraw(self, amount):
        """Removes amount from self.bank"""
        self.bank -= amount

    def deposit(self, amount):
        """Adds amount from self.bank"""
        self.bank += amount
