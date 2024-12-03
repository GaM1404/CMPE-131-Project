import random

# Constants for card values
CARD_VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

# Card class to represent a single card
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = CARD_VALUES[rank]

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class to manage the deck of cards
class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for rank in CARD_VALUES.keys()]
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

# Player class to represent a player (or dealer)
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def calculate_score(self):
        self.score = sum(card.value for card in self.hand)
        # Adjust for aces if the score is over 21
        ace_count = sum(1 for card in self.hand if card.rank == 'A')
        while self.score > 21 and ace_count > 0:
            self.score -= 10
            ace_count -= 1

    def add_card(self, card):
        self.hand.append(card)
        self.calculate_score()

    def reset_hand(self):
        self.hand = []
        self.score = 0
