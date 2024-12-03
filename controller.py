import pygame
from .model import Deck, Player
from .view import View

class Controller:
    def __init__(self):
        self.deck = Deck()
        self.player = Player("Player")
        self.dealer = Player("Dealer")
        self.view = View()
        self.is_game_over = False

    def deal_initial_cards(self):
        # Deal two cards to both the player and dealer
        self.player.add_card(self.deck.deal_card())
        self.player.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())
        self.dealer.add_card(self.deck.deal_card())

    def game_loop(self):
        clock = pygame.time.Clock()

        self.deal_initial_cards()

        while not self.is_game_over:
            self.view.draw_background()
            self.display_game_status()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Player hits
                        self.player.add_card(self.deck.deal_card())
                    if event.key == pygame.K_s:  # Player stands
                        self.dealer_turn()
                        self.check_winner()
                        self.is_game_over = True

            self.view.update()
            clock.tick(60)

    def display_game_status(self):
        # Show player and dealer hand
        self.view.draw_text(f"Player: {self.player.score}", 50, 50)
        self.view.draw_text(f"Dealer: {self.dealer.score}", 50, 150)
        self.draw_player_hand()
        self.draw_dealer_hand()

    def draw_player_hand(self):
        x, y = 50, 100
        for card in self.player.hand:
            self.view.draw_card(card, x, y)
            x += 80

    def draw_dealer_hand(self):
        x, y = 50, 200
        for card in self.dealer.hand:
            self.view.draw_card(card, x, y)
            x += 80

    def dealer_turn(self):
        while self.dealer.score < 17:
            self.dealer.add_card(self.deck.deal_card())

    def check_winner(self):
        if self.player.score > 21:
            self.view.display_message("Player busts! Dealer wins!")
        elif self.dealer.score > 21:
            self.view.display_message("Dealer busts! Player wins!")
        elif self.player.score > self.dealer.score:
            self.view.display_message("Player wins!")
        elif self.player.score < self.dealer.score:
            self.view.display_message("Dealer wins!")
        else:
            self.view.display_message("It's a tie!")
