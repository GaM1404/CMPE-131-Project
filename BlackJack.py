import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
import os
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
    def load_card_images(self):
        """Loads images of playing cards into a dictionary."""
        image_folder = "assets"  # Folder where card images are stored
        images = {}
        suits = ['H', 'D', 'S', 'C']  # Hearts, Diamonds, Spades, Clubs
        for rank in self.card_values.keys():
            for suit in suits:
                card_name = f"{rank}{suit}.png"
                try:
                    img = Image.open(os.path.join(image_folder, card_name))
                    img = img.resize((100, 140))  # Resize to fit the UI
                    images[f"{rank}{suit}"] = ImageTk.PhotoImage(img)
                except FileNotFoundError:
                    pass  # Handle missing files gracefully
        return images
    def reset_game(self):
        self.deck = list(self.card_values.keys()) * 4
        random.shuffle(self.deck)
        self.player_hands = [[self.deal_card(), self.deal_card()]]
        self.dealer_cards = [self.deal_card(), self.deal_card()]
        self.current_hand = 0

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

    def payout(self, multiplier):
        payout_amount = self.current_bet * multiplier
        self.player_money += payout_amount
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

        # Cards display
        self.player_cards_frame = tk.Frame(root)
        self.player_cards_frame.pack(pady=10)
        self.dealer_cards_frame = tk.Frame(root)
        self.dealer_cards_frame.pack(pady=10)

        # Button Controls
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", width=10, state="disabled")
        self.stand_button = tk.Button(self.button_frame, text="Stand", width=10, state="disabled")
        self.double_button = tk.Button(self.button_frame, text="Double Down", width=12, state="disabled")
        self.restart_button = tk.Button(self.button_frame, text="Restart", width=10)

        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button.pack(side=tk.LEFT, padx=5)
        self.double_button.pack(side=tk.LEFT, padx=5)
        self.restart_button.pack(side=tk.LEFT, padx=5)

    
    def update_player(self, hands, current_hand, scores):
        self.clear_cards(self.player_cards_frame)
        display_hands = ""
        for i, hand in enumerate(hands):
            display_hands += f"Hand {i + 1}: {' '.join(hand)} (Score: {scores[i]})\n"
            for card in hand:
                card_img = self.get_card_image(card)
                label = tk.Label(self.player_cards_frame, image=card_img)
                label.image = card_img  # Keep a reference to prevent garbage collection
                label.pack(side=tk.LEFT)
        self.player_label.config(text=f"Your cards:\n{display_hands}\n(Current Hand: {current_hand + 1})")

    def update_dealer(self, cards, reveal=False):
        self.clear_cards(self.dealer_cards_frame)
        if reveal:
            for card in cards:
                card_img = self.get_card_image(card)
                label = tk.Label(self.dealer_cards_frame, image=card_img)
                label.image = card_img  # Keep a reference to prevent garbage collection
                label.pack(side=tk.LEFT)
            self.dealer_label.config(text=f"Dealer's cards: {', '.join(cards)}")
        else:
            # Show only one dealer card (hidden second card)
            card_img = self.get_card_image(cards[0])
            label = tk.Label(self.dealer_cards_frame, image=card_img)
            label.image = card_img
            label.pack(side=tk.LEFT)
            self.dealer_label.config(text=f"Dealer's cards: {cards[0]}, ?")

    def get_card_image(self, card):
        """Return the appropriate card image from the model."""
        return self.model.card_images.get(card, None)

    def clear_cards(self, frame):
        """Clears the card images displayed in a frame."""
        for widget in frame.winfo_children():
            widget.destroy()
    def update_money(self, money):
        self.money_label.config(text=f"Money: ${money}")

    def display_result(self, result):
        self.result_label.config(text=result)

    def reset_result(self):
        self.result_label.config(text="")

    def set_buttons_state(self, hit="disabled", stand="disabled", double="disabled"):
        self.hit_button.config(state=hit)
        self.stand_button.config(state=stand)
        self.double_button.config(state=double)


# --- Controller ---
class BlackjackController:
    def __init__(self, root):
        self.model = BlackjackModel()
        self.view = BlackjackView(root)

        # Button bindings
        self.view.hit_button.config(command=self.hit)
        self.view.stand_button.config(command=self.stand)
        self.view.double_button.config(command=self.double_down)
        self.view.restart_button.config(command=self.restart)

        self.buy_in()

    def buy_in(self):
        buy_in_amount = simpledialog.askinteger("Buy In", "Enter your buy-in amount ($):", minvalue=1)
        if buy_in_amount:
            self.model.player_money = buy_in_amount
            self.restart()
        else:
            self.view.display_result("Buy-in is required to start the game.")

    def restart(self):
        self.model.reset_game()
        self.view.reset_result()
        self.view.set_buttons_state(hit="normal", stand="normal", double="normal")
        self.place_bet()

    def place_bet(self):
        bet_amount = simpledialog.askinteger("Place Bet", "Enter your bet amount ($):", minvalue=1, maxvalue=self.model.player_money)
        if bet_amount:
            try:
                self.model.place_bet(bet_amount)
                self.view.update_money(self.model.player_money)
                self.update_view()
            except ValueError as e:
                self.view.display_result(str(e))
                self.place_bet()
        else:
            self.view.display_result("Bet is required to continue.")

    def hit(self):
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        score = self.model.calculate_score(hand)
        self.update_view()
        if score > 21:
            self.view.display_result(f"Hand {self.model.current_hand + 1} Bust! Over 21.")
            self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled")
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
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        self.model.current_bet *= 2
        self.view.update_money(self.model.player_money)
        self.view.display_result(f"Hand {self.model.current_hand + 1} Double Down!")
        self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled")
        self.stand()

    def evaluate_winner(self):
        dealer_score = self.model.calculate_score(self.model.dealer_cards)
        results = []
        for i, hand in enumerate(self.model.player_hands):
            player_score = self.model.calculate_score(hand)
            if player_score > 21:
                results.append(f"Hand {i + 1}: Bust!")
            elif dealer_score > 21 or player_score > dealer_score:
                payout = 2.5 if len(hand) == 2 and player_score == 21 else 2
                self.model.payout(payout)
                results.append(f"Hand {i + 1}: You win! Payout: {payout}x")
            elif player_score < dealer_score:
                results.append(f"Hand {i + 1}: Dealer wins.")
            else:
                self.model.payout(1)  # Tie
                results.append(f"Hand {i + 1}: Tie. Bet returned.")
        self.view.update_money(self.model.player_money)
        self.view.display_result("\n".join(results))
        self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled")
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
