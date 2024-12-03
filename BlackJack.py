import tkinter as tk
from tkinter import simpledialog
import random
from PIL import Image, ImageTk
import os


# --- Model ---
class BlackjackModel:
    def __init__(self):
        suits = ['S', 'H', 'D', 'C']  # Spades, Hearts, Diamonds, Clubs
        self.card_values = {
            '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
            '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11
        }
        self.deck = [f"{rank}{suit}" for rank in self.card_values.keys() for suit in suits]
        self.player_hands = []
        self.dealer_cards = []
        self.current_hand = 0
        self.player_money = 0
        self.current_bet = 0
        self.split_bet = 0

    def reset_game(self):
        self.deck = [f"{rank}{suit}" for rank in self.card_values.keys() for suit in ['S', 'H', 'D', 'C']]
        random.shuffle(self.deck)
        self.player_hands = [[self.deal_card(), self.deal_card()]]
        self.dealer_cards = [self.deal_card(), self.deal_card()]
        self.current_hand = 0
        self.split_bet = 0

    def deal_card(self):
        return self.deck.pop()

    def calculate_score(self, cards):
        ranks = [card[:-1] for card in cards]
        score = sum(self.card_values[rank] for rank in ranks)
        aces = ranks.count('A')
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

        self.player_label = tk.Label(root, text="Your cards:", font=("Helvetica", 14))
        self.dealer_label = tk.Label(root, text="Dealer's cards:", font=("Helvetica", 14))
        self.money_label = tk.Label(root, text="Money: $0", font=("Helvetica", 14), fg="green")
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red")

        self.player_label.pack(pady=10)
        self.dealer_label.pack(pady=10)
        self.money_label.pack(pady=10)
        self.result_label.pack(pady=10)

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

        # Create frames to hold card images
        self.player_cards_frame = tk.Frame(root)
        self.player_cards_frame.pack(pady=10)
        self.dealer_cards_frame = tk.Frame(root)
        self.dealer_cards_frame.pack(pady=10)

        self.player_card_images = []
        self.dealer_card_images = []

    def load_card_image(self, card):
        image_path = os.path.join('assets', f'{card}.png')
        try:
            img = Image.open(image_path)
            img = img.resize((50, 75))
            return ImageTk.PhotoImage(img)
        except FileNotFoundError:
            return None

    def update_player(self, hands, current_hand, scores):
        # Display player cards in text
        hand_text = ", ".join(hands[current_hand])
        self.player_label.config(text=f"Your cards: {hand_text} (Score: {scores[current_hand]})")

        # Display player card images
        self.clear_player_images()
        for card in hands[current_hand]:
            img = self.load_card_image(card)
            if img:
                self.player_card_images.append(img)

        # Clear previous images and display new ones
        self.display_card_images(self.player_cards_frame, self.player_card_images)

    def update_dealer(self, cards, reveal=False):
    # If reveal is False (i.e., during the player's turn), only show the first card
        if not reveal:
            dealer_text = f"Dealer's cards: {cards[0]}, ?"
            self.dealer_label.config(text=dealer_text)
            
            # Display only the first card of the dealer
            self.clear_dealer_images()
            first_card_img = self.load_card_image(cards[0])
            if first_card_img:
                self.dealer_card_images.append(first_card_img)
            
            # Display the first card image
            self.display_card_images(self.dealer_cards_frame, self.dealer_card_images)
        else:
            # After the player's action (reveal all dealer cards)
            dealer_text = ", ".join(cards)
            self.dealer_label.config(text=f"Dealer's cards: {dealer_text}")
            
            # Display all the dealer's cards
            self.clear_dealer_images()
            for card in cards:
                img = self.load_card_image(card)
                if img:
                    self.dealer_card_images.append(img)
            
            # Display all dealer card images
            self.display_card_images(self.dealer_cards_frame, self.dealer_card_images)

    def display_card_images(self, frame, images):
        for widget in frame.winfo_children():
            widget.destroy()  # Clear previous images

        for img in images:
            label = tk.Label(frame, image=img)
            label.pack(side=tk.LEFT, padx=5)

    def clear_player_images(self):
        self.player_card_images = []

    def clear_dealer_images(self):
        self.dealer_card_images = []

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



class BlackjackController:
    def __init__(self, root):
        self.model = BlackjackModel()
        self.view = BlackjackView(root)

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

    def rebuy(self):
        rebuy_amount = simpledialog.askinteger("Rebuy", "Enter your rebuy amount ($):", minvalue=1)
        if rebuy_amount:
            self.model.player_money += rebuy_amount
            self.view.update_money(self.model.player_money)
            self.view.display_result("Rebuy successful! You can now place a bet.")
            self.view.set_buttons_state(play="normal", rebuy="disabled")
        else:
            self.view.display_result("Rebuy canceled.")

    def play(self):
        if self.model.player_money > 0:
            self.model.reset_game()
            self.view.reset_result()
            self.place_bet()
        else:
            self.view.set_buttons_state(play="disabled", rebuy="normal")
            self.view.display_result("Out of money! Please rebuy to continue.")

    def place_bet(self):
        bet_amount = simpledialog.askinteger("Place Bet", "Enter your bet amount ($):", minvalue=1, maxvalue=self.model.player_money)
        if bet_amount:
            try:
                self.model.place_bet(bet_amount)
                self.view.update_money(self.model.player_money)
                self.update_view()
                self.check_blackjack()
                self.view.set_buttons_state(hit="normal", stand="normal", double="normal", split="normal")
            except ValueError as e:
                self.view.display_result(str(e))
                self.place_bet()
        else:
            self.view.display_result("Bet is required to continue.")

    def check_blackjack(self):
        hand = self.model.player_hands[0]
        score = self.model.calculate_score(hand)
        if score == 21:
            self.model.payout(1.5)
            self.view.update_money(self.model.player_money)
            self.view.display_result("Blackjack! You win 3:2 payout!")
            self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled", split="disabled", play="normal")
            self.update_view(reveal=True)

    def hit(self):
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        self.update_view()
        if self.model.calculate_score(hand) > 21:
            self.view.display_result(f"Hand {self.model.current_hand + 1} Bust!")
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
        if len(hand) == 2 and self.model.player_money >= self.model.current_bet:
            self.model.player_money -= self.model.current_bet
            if self.model.current_hand == 0:
                self.model.current_bet *= 2
            else:
                self.model.split_bet *= 2
            self.view.update_money(self.model.player_money)
            hand.append(self.model.deal_card())
            self.view.display_result("Double Down!")
            self.view.set_buttons_state(hit="disabled", stand="disabled", double="disabled", split="disabled")
            self.stand()
        else:
            self.view.display_result("Double Down is only allowed on your first two cards!")

    def split(self):
        hand = self.model.player_hands[self.model.current_hand]
        if len(hand) == 2 and self.model.card_values[hand[0][:-1]] == self.model.card_values[hand[1][:-1]] and self.model.player_money >= self.model.current_bet:
            self.model.player_money -= self.model.current_bet
            self.model.split_bet = self.model.current_bet
            self.model.player_hands.append([hand.pop()])
            hand.append(self.model.deal_card())
            self.model.player_hands[-1].append(self.model.deal_card())
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
            bet_amount = self.model.current_bet if i == 0 else self.model.split_bet
            if player_score > 21:
                results.append(f"Hand {i + 1}: Bust! You lose ${bet_amount}.")
            elif dealer_score > 21 or player_score > dealer_score:
                self.model.payout(2, split=(i > 0))
                results.append(f"Hand {i + 1}: Win! You win ${bet_amount * 2}.")
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
<<<<<<< HEAD
    root.mainloop()
=======
    root.mainloop()

>>>>>>> cd1e03132022960fef6356d53db8980f385da23a
