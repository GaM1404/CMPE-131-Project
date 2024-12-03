import tkinter as tk
from tkinter import simpledialog
import random


# --- Model ---
class BlackjackModel:
    def __init__(self):
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }
        self.deck = []
        self.player_hands = []
        self.dealer_cards = []
        self.current_hand = 0
        self.player_money = 0
        self.current_bet = 0
        self.split_bet = 0

    def reset_game(self):
        self.deck = list(self.card_values.keys()) * 4
        random.shuffle(self.deck)
        self.player_hands = [[self.deal_card(), self.deal_card()]]
        self.dealer_cards = [self.deal_card(), self.deal_card()]
        self.current_hand = 0
        self.split_bet = 0

    def deal_card(self):
        return self.deck.pop()

    def calculate_score(self, cards):
        score = sum(self.card_values[card] for card in cards)
        aces = cards.count('A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def place_bet(self, bet_amount):
        if bet_amount <= self.player_money:
            self.player_money -= bet_amount
            self.current_bet = bet_amount
        else:
            raise ValueError("Insufficient funds!")

    def payout(self, multiplier, split=False):
        payout_amount = (self.split_bet if split else self.current_bet) * multiplier
        self.player_money += payout_amount
        if split:
            self.split_bet = 0
        else:
            self.current_bet = 0


# --- View ---
class BlackjackView:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Game")

        # Game Information Labels
        self.player_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.dealer_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.money_label = tk.Label(root, text="Money: $0", font=("Helvetica", 14), fg="green")
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red")

        self.player_label.pack(pady=10)
        self.dealer_label.pack(pady=10)
        self.money_label.pack(pady=10)
        self.result_label.pack(pady=10)

        # Button Controls
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", width=10, state="disabled")
        self.stand_button = tk.Button(self.button_frame, text="Stand", width=10, state="disabled")
        self.double_button = tk.Button(self.button_frame, text="Double Down", width=12, state="disabled")
        self.split_button = tk.Button(self.button_frame, text="Split", width=10, state="disabled")
        self.play_button = tk.Button(self.button_frame, text="Play", width=10)
        self.rebuy_button = tk.Button(self.button_frame, text="Rebuy", width=10, state="disabled")

        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button.pack(side=tk.LEFT, padx=5)
        self.double_button.pack(side=tk.LEFT, padx=5)
        self.split_button.pack(side=tk.LEFT, padx=5)
        self.play_button.pack(side=tk.LEFT, padx=5)
        self.rebuy_button.pack(side=tk.LEFT, padx=5)

    def update_player(self, hands, current_hand, scores):
        display_hands = "\n".join(
            [f"Hand {i + 1}: {', '.join(hand)} (Score: {scores[i]})" for i, hand in enumerate(hands)]
        )
        self.player_label.config(text=f"Your cards:\n{display_hands}\n(Current Hand: {current_hand + 1})")

    def update_dealer(self, cards, reveal=False):
        if reveal:
            self.dealer_label.config(text=f"Dealer's cards: {', '.join(cards)}")
        else:
            self.dealer_label.config(text=f"Dealer's cards: {cards[0]}, ?")

    def update_money(self, money):
        self.money_label.config(text=f"Money: ${money}")

    def display_result(self, result):
        self.result_label.config(text=result)

    def reset_result(self):
        self.result_label.config(text="")

    def set_buttons_state(self, hit="disabled", stand="disabled", double="disabled", split="disabled", play="normal", rebuy="disabled"):
        self.hit_button.config(state=hit)
        self.stand_button.config(state=stand)
        self.double_button.config(state=double)
        self.split_button.config(state=split)
        self.play_button.config(state=play)
        self.rebuy_button.config(state=rebuy)


# --- Controller ---
class BlackjackController:
    def __init__(self, root):
        self.model = BlackjackModel()
        self.view = BlackjackView(root)

        # Button bindings
        self.view.hit_button.config(command=self.hit)
        self.view.stand_button.config(command=self.stand)
        self.view.double_button.config(command=self.double_down)
        self.view.split_button.config(command=self.split)
        self.view.play_button.config(command=self.play)
        self.view.rebuy_button.config(command=self.rebuy)

        self.buy_in()

    def buy_in(self):
        buy_in_amount = simpledialog.askinteger("Buy In", "Enter your buy-in amount ($):", minvalue=1)
        if buy_in_amount:
            self.model.player_money = buy_in_amount
            self.play()
        else:
            self.view.display_result("Buy-in is required to start the game.")

    def play(self):
        if self.model.player_money > 0:
            self.model.reset_game()
            self.view.reset_result()
            self.view.set_buttons_state(hit="normal", stand="normal", double="normal", split="normal", play="disabled")
            self.place_bet()
        else:
            self.view.set_buttons_state(play="disabled", rebuy="normal")
            self.view.display_result("Out of money! Please rebuy to continue.")

    def rebuy(self):
        self.buy_in()

    def place_bet(self):
        bet_amount = simpledialog.askinteger("Place Bet", "Enter your bet amount ($):", minvalue=1, maxvalue=self.model.player_money)
        if bet_amount:
            try:
                self.model.place_bet(bet_amount)
                self.view.update_money(self.model.player_money)
                self.update_view()
                self.check_blackjack()
            except ValueError as e:
                self.view.display_result(str(e))
                self.place_bet()
        else:
            self.view.display_result("Bet is required to continue.")

    def check_blackjack(self):
        hand = self.model.player_hands[0]
        score = self.model.calculate_score(hand)
        if score == 21:
            self.model.payout(1.5)  # Blackjack payout is 3:2
            self.view.update_money(self.model.player_money)
            self.view.display_result("Blackjack! You win 3:2 payout!")
            self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled", split="disabled", play="normal")
            self.update_view(reveal=True)

    def hit(self):
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        score = self.model.calculate_score(hand)
        self.update_view()
        if score > 21:
            self.view.display_result(f"Hand {self.model.current_hand + 1} Bust! Over 21.")
            self.stand()

    def stand(self):
        if self.model.current_hand < len(self.model.player_hands) - 1:
            self.model.current_hand += 1
            self.update_view()
        else:
            while self.model.calculate_score(self.model.dealer_cards) < 17:
                self.model.dealer_cards.append(self.model.deal_card())
            self.evaluate_winner()

    def double_down(self):
        if self.model.player_money >= self.model.current_bet:
            self.model.player_money -= self.model.current_bet
            self.model.current_bet *= 2
            self.view.update_money(self.model.player_money)

            hand = self.model.player_hands[self.model.current_hand]
            hand.append(self.model.deal_card())
            self.view.display_result("Double Down!")
            self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled", split="disabled")
            self.stand()
        else:
            self.view.display_result("Not enough money to Double Down!")

    def split(self):
        hand = self.model.player_hands[self.model.current_hand]
        if len(hand) == 2 and self.model.card_values[hand[0]] == self.model.card_values[hand[1]] and self.model.player_money >= self.model.current_bet:
            self.model.player_money -= self.model.current_bet  # Deduct additional bet
            self.model.split_bet = self.model.current_bet  # Set the split bet
            self.model.player_hands.append([hand.pop()])  # Move one card to a new hand
            hand.append(self.model.deal_card())  # Deal new card to first hand
            self.model.player_hands[-1].append(self.model.deal_card())  # Deal new card to split hand
            self.view.update_money(self.model.player_money)
            self.update_view()
            self.view.display_result("Split successful!")
        else:
            self.view.display_result("Cannot Split! Cards must have the same value and sufficient funds.")

    def evaluate_winner(self):
        dealer_score = self.model.calculate_score(self.model.dealer_cards)
        results = []
        for i, hand in enumerate(self.model.player_hands):
            player_score = self.model.calculate_score(hand)
            bet_amount = self.model.current_bet if i == 0 else self.model.split_bet  # Use correct bet for split hands
            if player_score > 21:
                results.append(f"Hand {i + 1}: Bust! You lose ${bet_amount}.")
            elif dealer_score > 21 or player_score > dealer_score:
                multiplier = 2
                self.model.payout(multiplier, split=(i > 0))
                win_amount = bet_amount * multiplier
                results.append(f"Hand {i + 1}: Win! You win ${win_amount}.")
            elif player_score < dealer_score:
                results.append(f"Hand {i + 1}: Dealer wins! You lose ${bet_amount}.")
            else:
                self.model.payout(1, split=(i > 0))
                results.append(f"Hand {i + 1}: Tie! Bet returned.")
        self.view.update_money(self.model.player_money)
        self.view.display_result("\n".join(results))
        self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled", split="disabled", play="normal")
        self.update_view(reveal=True)

    def update_view(self, reveal=False):
        scores = [self.model.calculate_score(hand) for hand in self.model.player_hands]
        self.view.update_player(self.model.player_hands, self.model.current_hand, scores)
        self.view.update_dealer(self.model.dealer_cards, reveal)


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackController(root)
    root.mainloop()
