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

# initializes player 1
player1_hand = Hand()
player1 = BlackjackPlayer("Player 1", player1_hand, 100)

# initializes player 2
player2_hand = Hand()
player2 = BlackjackPlayer("Player 2", player2_hand, 100)

# initializes dealer
dealer_hand = Hand()
dealer = Dealer("Dealer", dealer_hand, 1000000000000)

another_round = 'Y'
while another_round == 'Y':
    # gives out new cards
    player1.get_card(deck.deal_card())
    player1.get_card(deck.deal_card())

    player2.get_card(deck.deal_card())
    player2.get_card(deck.deal_card())

    dealer.get_card(deck.deal_card())
    dealer.get_card(deck.deal_card())

    print("Time for everyone to place their bet!")
    print("-----------------------")

    # gets bets going
    player1_bet = int(input(f"{player1.name}, how much would you like to bet? "))
    player2_bet = int(input(f"{player2.name}, how much would you like to bet? "))
    print(f"{player1.name} bets ${player1_bet}")
    print(f"{player2.name} bets ${player2_bet}")

    player1.place_bet(player1_bet)
    player2.place_bet(player2_bet)

    print("The initial starting cards are:")
    print("--------------------------------")

    # prints initial starting hands
    print(f"{player1.name}'s current hand: ", end="")
    player1.hand.print_facedown()

    print(f"{player2.name}'s current hand: ", end="")
    player2.hand.print_facedown()

    print(f"{dealer.name}'s current hand: ", end="")
    dealer.hand.print_facedown()

    # players and dealer play
    player1.play(deck)
    player2.play(deck)
    dealer.play(deck)

    # determine winners and update balances
    # player 1 tie condidtion
    if (player1.value() == dealer.value() or (player1.is_busted() and dealer.is_busted())):
        print(f"It's a tie! {player1.name} loses $0")
        player1.win_bet(player1_bet)
    # player 1 lose condition
    elif (player1.is_busted() or dealer.value() > player1.value() and not dealer.is_busted()):
        print(f"Oof! {player1.name} loses ${player1_bet}")
        dealer.win_bet(player1_bet)
    # player 1 win condition
    else:
        print(f"Bang! {player1.name} wins ${player1_bet}")
        player1.win_bet(player1_bet * 2)
        dealer.money -= player1_bet
    # player 2 tie condidtion
    if (player2.value() == dealer.value() or (player2.is_busted() and dealer.is_busted())):
        print(f"It's a tie! {player2.name} loses $0")
        player2.win_bet(player2_bet)
    # player 2 lose condition
    elif (player2.is_busted() or dealer.value() > player2.value() and not dealer.is_busted()):
        print(f"Oof! {player2.name} loses ${player2_bet}")
        dealer.win_bet(player2_bet)
    # player 2 win condition
    else:
        print(f"Bang! {player2.name} wins ${player2_bet}")
        player2.win_bet(player2_bet * 2)
        dealer.money -= player2_bet
    
    print("The standings so far:")
    print("--------------------")

    # prints player and dealer standings
    print(f"{player1.name} ${player1.money}")
    print(f"{player2.name} ${player2.money}")
    print(f"{dealer.name} is up ${dealer.money}")

    # resets hands
    player1.reset()
    player2.reset()
    dealer.reset()

    # prompts user for another round
    another_round = input("Another round? (Y or N): ")