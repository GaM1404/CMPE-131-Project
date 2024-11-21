import random

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck

def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card, _ in hand:
        if card in ['Jack', 'Queen', 'King']:
            value += 10
        elif card == 'Ace':
            aces += 1
            value += 11
        else:
            value += int(card)

    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

def display_hand(hand, hide_first_card=False):
    if hide_first_card:
        print("[Hidden Card]", hand[1])
    else:
        for card in hand:
            print(card)

def blackjack():
    deck = create_deck()
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    while True:
        print("\nYour Hand:")
        display_hand(player_hand)
        print("Value:", calculate_hand_value(player_hand))
        
        print("\nDealer's Hand:")
        display_hand(dealer_hand, hide_first_card=True)

        if calculate_hand_value(player_hand) == 21:
            print("Blackjack! You win!")
            return

        action = input("Do you want to hit or stand? Press h for hit and s for stand:").strip().lower()
        if action == 'h':
            player_hand.append(deck.pop())
            if calculate_hand_value(player_hand) > 21:
                print("\nYour Hand:")
                display_hand(player_hand)
                print("Value:", calculate_hand_value(player_hand))
                print("Bust! You lose!")
                return
        elif action == 's':
            break

    print("\nDealer's Hand:")
    display_hand(dealer_hand)
    
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        print("\nDealer hits.")
        display_hand(dealer_hand)

    player_value = calculate_hand_value(player_hand)
    dealer_value = calculate_hand_value(dealer_hand)

    print("\nFinal Hands:")
    print("Your Hand:", player_hand, "Value:", player_value)
    print("Dealer's Hand:", dealer_hand, "Value:", dealer_value)

    if dealer_value > 21 or player_value > dealer_value:
        print("You win!")
    elif player_value < dealer_value:
        print("You lose!")
    else:
        print("It's a tie!")

print("Welcome to Blackjack!")
conidtion = True
while True:
    if __name__ == "__main__":
        blackjack()

    print("Do you want to play again? Press 'y' for Yes and 'n' for No:")
    condition = input().strip().lower() == 'y'
    if not condition:
        break
