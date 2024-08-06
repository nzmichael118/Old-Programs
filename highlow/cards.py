"""Stores basic functions and values associated with a deck of cards"""

import random

class Card():
    """Card struct stores information of a card"""

    def __init__(self, type_value, value):
        """int type: 1 - 4, int value: 1-13"""
        labels = \
        ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        types = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        # Assign
        self.label = labels[value] 
        self.type = types[type_value]
        self.value = value
        

    def __str__(self):
        """Returns label of type e.g. 'Queen of Hearts'"""
        return(f'{self.label} of {self.type}')


class Deck():
    """Stores multiple cards"""
    
    def __init__(self, deck_count):
        """int: deck_count"""
        self.deck_count = deck_count
        self.cards = []
        self.replace_deck()
        self.shuffle_deck()


    def replace_deck(self):
        new_cards = []
        for i in range(self.deck_count):
            for types in range(4):
                for values in range(13):
                    new_cards.append(Card(types, values))
        
        self.cards = new_cards
        return(new_cards)


    def shuffle_deck(self):
        """Shuffles the deck"""
        random.shuffle(self.cards)


    def draw_card(self):
        """returns top card and removes it from the deck and if deck is reshuffled returns true
        can use this True return as a visualisation later"""
        try:
            # .pop() removes and *returns* last item
            return(self.cards.pop(), False)
        except IndexError:
            # Deck is empty replace and shuffle
            self.replace_deck()
            self.shuffle_deck()
            return(self.cards.pop(), True)