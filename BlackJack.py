import tkinter as tk
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
        self.player_hands = []  # Player can have multiple hands due to splits
        self.dealer_cards = []
        self.current_hand = 0

    def reset_game(self):
        self.deck = list(self.card_values.keys()) * 4
        random.shuffle(self.deck)
        self.player_hands = [[self.deal_card(), self.deal_card()]]
        self.dealer_cards = [self.deal_card(), self.deal_card()]
        self.current_hand = 0

    def deal_card(self):
        return random.choice(self.deck)

    def calculate_score(self, cards):
        score = sum(self.card_values[card] for card in cards)
        aces = cards.count('A')
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def split_hand(self):
        if len(self.player_hands[0]) == 2 and self.player_hands[0][0] == self.player_hands[0][1]:
            card = self.player_hands[0].pop()
            self.player_hands.append([card, self.deal_card()])
            self.player_hands[0].append(self.deal_card())


# --- View ---
class BlackjackView:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack")

        # Labels
        self.player_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.dealer_label = tk.Label(root, text="", font=("Helvetica", 14))
        self.result_label = tk.Label(root, text="", font=("Helvetica", 14), fg="red")

        self.player_label.pack(pady=10)
        self.dealer_label.pack(pady=10)
        self.result_label.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=20)

        self.hit_button = tk.Button(self.button_frame, text="Hit", width=10)
        self.stand_button = tk.Button(self.button_frame, text="Stand", width=10)
        self.double_button = tk.Button(self.button_frame, text="Double Down", width=12)
        self.split_button = tk.Button(self.button_frame, text="Split", width=10)
        self.restart_button = tk.Button(self.button_frame, text="Restart", width=10)

        self.hit_button.pack(side=tk.LEFT, padx=5)
        self.stand_button.pack(side=tk.LEFT, padx=5)
        self.double_button.pack(side=tk.LEFT, padx=5)
        self.split_button.pack(side=tk.LEFT, padx=5)
        self.restart_button.pack(side=tk.LEFT, padx=5)

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

    def display_result(self, result):
        self.result_label.config(text=result)

    def reset_result(self):
        self.result_label.config(text="")

    def set_buttons_state(self, state):
        self.hit_button.config(state=state)
        self.double_button.config(state=state)
        self.stand_button.config(state=state)
        self.split_button.config(state=state)


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
        self.view.restart_button.config(command=self.restart)

        self.restart()

    def restart(self):
        self.model.reset_game()
        self.view.reset_result()
        self.view.set_buttons_state("normal")
        self.update_view()

    def hit(self):
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        score = self.model.calculate_score(hand)
        self.update_view()
        if score > 21:
            self.view.display_result(f"Hand {self.model.current_hand + 1} Bust! Over 21.")
            self.disable_buttons_for_hand()
            self.stand()

    def stand(self):
        if self.model.current_hand < len(self.model.player_hands) - 1:
            self.model.current_hand += 1
            self.view.set_buttons_state("normal")
            self.update_view()
        else:
            while self.model.calculate_score(self.model.dealer_cards) < 17:
                self.model.dealer_cards.append(self.model.deal_card())
            self.evaluate_winner()

    def double_down(self):
        hand = self.model.player_hands[self.model.current_hand]
        hand.append(self.model.deal_card())
        score = self.model.calculate_score(hand)
        self.view.display_result(f"Hand {self.model.current_hand + 1} Double Down!")
        self.disable_buttons_for_hand()
        self.stand()

    def split(self):
        if len(self.model.player_hands[0]) == 2 and self.model.player_hands[0][0] == self.model.player_hands[0][1]:
            self.model.split_hand()
            self.update_view()
        else:
            self.view.display_result("Split not possible.")

    def evaluate_winner(self):
        dealer_score = self.model.calculate_score(self.model.dealer_cards)
        results = []
        for i, hand in enumerate(self.model.player_hands):
            player_score = self.model.calculate_score(hand)
            if player_score > 21:
                results.append(f"Hand {i + 1}: Bust!")
            elif dealer_score > 21 or player_score > dealer_score:
                results.append(f"Hand {i + 1}: You win!")
            elif player_score < dealer_score:
                results.append(f"Hand {i + 1}: Dealer wins.")
            else:
                results.append(f"Hand {i + 1}: It's a tie.")
        self.view.display_result("\n".join(results))
        self.view.set_buttons_state("disabled")
        self.update_view(reveal=True)

    def update_view(self, reveal=False):
        scores = [self.model.calculate_score(hand) for hand in self.model.player_hands]
        self.view.update_player(self.model.player_hands, self.model.current_hand, scores)
        self.view.update_dealer(self.model.dealer_cards, reveal)

    def disable_buttons_for_hand(self):
        self.view.set_buttons_state("disabled")


# --- Main ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BlackjackController(root)
    root.mainloop()
