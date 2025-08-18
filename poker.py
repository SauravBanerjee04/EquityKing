import random

players = 4
player_cards = [[] for player in range(players)]
community_cards = []
# Every rank
ranks = ['2', '3', '4', '5', '6', '7', '8','9','10','J','Q','K','A']
# Hearts, Diamonds, Spades, Clubs

suits = ['H','D','S','C']

# Create the deck
deck = [(rank, suit) for rank in ranks for suit in suits]
random.shuffle(deck)
random.shuffle(deck)
print(deck)


print(player_cards)

for x in range(0,players*2): #deal out cards to players
    player_cards[x % players].append(deck.pop(0))
