import random

class Card:
    SUITS = ['C', 'H', 'D', 'S']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    VALUES = {'A':[1, 11], '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'J':10, 'Q':10, 'K':10}

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def get_value(self):
        return self.VALUES[self.rank]

    def __str__(self):
        return f"{self.rank}{self.suit}"

'''
# card testing
card1 = Card('A', 'S')
card2 = Card('5', 'H')
card3 = Card('A', 'C')
print(card1)
print(card1.get_value())
print()
'''

class Hand:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card):
        self.cards.append(card)
    
    def clear_hand(self):
        self.cards = []
    
    def get_total(self):
        total = 0
        ace_count = 0
        for card in self.cards:
            if (card.rank == 'A'):
                ace_count += 1
                total += card.get_value()[1]
            else:
                total += card.get_value()

        while total > 21 and ace_count > 0:
            total -= 10
            ace_count -= 1
        
        return total

    def print_facedown(self):
        result = "[??]"
        for i in range(1, (len(self.cards))):
            result = f"{result}[{self.cards[i]}]"
        print(result)

    def __str__(self):
        result = ""
        for card in self.cards:
            result += f"[{card}]"
        return result

    def get_size(self):
        return len(self.cards)

'''
# hand testing
hand1 = Hand()
hand1.add_card(card1)
hand1.add_card(card2)
hand1.add_card(card3)
hand1.print_facedown()
print(hand1.get_size())
print(hand1.get_total())
print(hand1)
hand1.clear_hand()
print(hand1)
print()
'''

class Deck:
    def __init__(self, deck_count):
        self.deck_count = deck_count
        self.cards = self.generate_deck()
    
    def generate_deck(self):
        base_deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                base_deck.append(Card(rank, suit))
        base_deck *= self.deck_count
        random.shuffle(base_deck)
        return base_deck
    
    def deal_card(self):
        if (self.needs_refill()):
            self.refill()
        return self.cards.pop(0)
    
    # checks if the deck has >= 20 cards in it
    def needs_refill(self):
        if (len(self.cards) <= 20):
            return True
        else:
            return False
    
    def refill(self):
        self.cards = self.generate_deck()

'''
# deck testing
deck1 = Deck()
for i in range(0, 10):
    print(deck1.deal_card())
deck1.shuffle()
print()
for i in range(0, 10):
    print(deck1.deal_card())
print()
'''

class Player:
    def __init__(self, name, hand, money):
        self.name = name
        self.hand = hand
        self.money = money
    
    def place_bet(self, amount):
        self.money -= amount

    def win_bet(self, amount):
        self.money += amount
    
    def is_busted(self):
        if (self.hand.get_total() > 21):
            return True
        else:
            return False
    
    def get_card(self, card):
        self.hand.add_card(card)
        
    def reset(self):
        self.hand.clear_hand()
    
    def value(self):
        return self.hand.get_total()

class BlackjackPlayer(Player):
    def play(self, deck):
        draw_another = 'Y'

        print(f"{self.name}'s turn:")
        print("-------------------")

        print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
        while draw_another == 'Y':
            draw_another = input("Would you like to draw another card? (Y or N): ")
            if (draw_another == 'Y'):
                print(f"{self.name} chooses to draw")
                self.get_card(deck.deal_card())
                if (not self.is_busted()):
                    print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
                else:
                    print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
                    print(f"{self.name} has busted")
                    break
            else:
                print(f"{self.name} chooses to stay")
                break

class Dealer(Player):
    def play(self, deck):
        print(f"{self.name}'s turn:")
        print("-------------------")

        print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
        while True:
            if (self.value() < 17):
                print(f"{self.name} chooses to draw")
                self.get_card(deck.deal_card())
                if (not self.is_busted()):
                    print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
                else:
                    print(f"{self.name}'s current hand: {self.hand} ({self.value()} points)")
                    print(f"{self.name} has busted")
                    break
            else:
                print(f"{self.name} chooses to stay")
                break
        
        print("Let's see how it turned out:")
        print("----------------------------")

# initializes some game stuff
print(f"Welcome to Blackjack!")
num_decks = int(input("How many decks do you want to use? "))
deck = Deck(num_decks)

# Ask how many players will participate
num_players = int(input("How many players will be playing?: "))
players = []

# Initialize players dynamically
for i in range(1, num_players + 1):
    player_hand = Hand()
    player = BlackjackPlayer(f"Player {i}", player_hand, 100)
    players.append(player)

# Initialize the dealer
dealer_hand = Hand()
dealer = Dealer("Dealer", dealer_hand, 1000000000000)

another_round = 'Y'
while another_round == 'Y':
    # Deal initial cards to all players
    for player in players:
        player.get_card(deck.deal_card())
        player.get_card(deck.deal_card())

    dealer.get_card(deck.deal_card())
    dealer.get_card(deck.deal_card())

    print("Time for everyone to place their bet!")
    print("-----------------------")

    # Get bets from all players
    bets = {}
    for player in players:
        player_bet = int(input(f"{player.name}, how much would you like to bet? "))
        print(f"{player.name} bets ${player_bet}")
        player.place_bet(player_bet)
        bets[player] = player_bet

    print("The initial starting cards are:")
    print("--------------------------------")

    # Print initial hands for all players
    for player in players:
        print(f"{player.name}'s current hand: ", end="")
        player.hand.print_facedown()

    print(f"{dealer.name}'s current hand: ", end="")
    dealer.hand.print_facedown()

    # Players take their turns
    for player in players:
        player.play(deck)

    # Dealer takes their turn
    dealer.play(deck)

    # Determine winners and update balances
    for player in players:
        player_bet = bets[player]
        if (player.value() == dealer.value() or (player.is_busted() and dealer.is_busted())):
            print(f"It's a tie! {player.name} loses $0")
            player.win_bet(player_bet)
        elif (player.is_busted() or dealer.value() > player.value() and not dealer.is_busted()):
            print(f"Oof! {player.name} loses ${player_bet}")
            dealer.win_bet(player_bet)
        else:
            print(f"Bang! {player.name} wins ${player_bet}")
            player.win_bet(player_bet * 2)
            dealer.money -= player_bet

    print("The standings so far:")
    print("--------------------")

    # Print standings for all players
    for player in players:
        print(f"{player.name} ${player.money}")
    print(f"{dealer.name} is up ${dealer.money}")

    # Reset hands for all players and dealer
    for player in players:
        player.reset()
    dealer.reset()

    # Prompt for another round
    another_round = input("Another round? (Y or N): ")