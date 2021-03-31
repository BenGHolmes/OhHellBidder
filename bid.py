import numpy as np
import random
import copy
import time

# Deck of cards. Order 2D, 2C, 2H, 2S, 3D, ... AH, AS
DECK = list(range(52))
VALUES = ['2', '3', '4', '5', '6', '7', '8' ,'9', '10', 'J', 'Q', 'K', 'A']
SUITS = 'DCHS'


"""
TODO:
    Return mode of tricks taken and probability of getting each number of tricks
    rather than average trick value

"""


def parse_hand(hand_str):
    hand_list = hand_str.split(" ")
    hand = []
    for card in hand_list:
        card_int = VALUES.index(card[:-1])*4 + SUITS.index(card[-1]) 
        hand.append(card_int)

    return hand


def fill_missing(trump, hand, n_players, pos):
    available_cards = DECK.copy()
    available_cards.remove(trump)
    for card in hand:
        available_cards.remove(card)

    n_cards = len(hand)

    hands = []
    for i in range(n_players):
        if i == pos:
            hands.append(hand.copy())
        else:
            npc_hand = random.sample(available_cards, n_cards)
            for card in npc_hand:
                available_cards.remove(card)
            hands.append(npc_hand)

    return hands


def check_winner(trump, lead, plays):
    trump = [x if x%4 == trump%4 else -1 for x in plays]
    if max(trump) >= 0:
        return np.argmax(trump)
    else:
        return np.argmax([x if x%4 == lead%4 else -1 for x in plays])


def play_hand(trump, hands, n_players):
    tricks = [0]*n_players

    for hand in hands:
        random.shuffle(hand)

    winner = 0
    for r in range(len(hands[0])):
        plays = [-1]*n_players
        # Winner leads with random card
        lead = hands[winner].pop(0)
        lead_suit = lead%4
        plays[winner] = lead
        
        for i in range(1,n_players):
            player = (winner+i)%n_players
            try:
                play = hands[player].pop([x%4 for x in hands[player]].index(lead%4))
            except ValueError:
                play = hands[player].pop(0)
            plays[player] = play

        winner = check_winner(trump, lead_suit, plays)
        tricks[winner] += 1

    return tricks


def mean_tricks(trump, hand, n_players, pos, n_hands, n_repeat, time_limit=None):
    tricks_taken = 0
    start = time.time()
    for i in range(n_hands):
        hands = fill_missing(trump, hand, n_players, pos)
        for j in range(n_repeat):
            tricks = play_hand(trump, copy.deepcopy(hands), n_players)
            tricks_taken += tricks[pos]
        
        if time_limit and (time.time()-start) > time_limit:
            break

    runtime = time.time()-start
    N = (i+1)*(j+1)
    avg_tricks = tricks_taken/N
    
    return avg_tricks, N, runtime


def play_game(n_players, pos, n_hands, n_repeat, time_limit=None):
    for i in range(13):
        print(f'Hand {i+1}. Position {pos}')
        trump = parse_hand(input("Trump card: "))[0]
        hand = parse_hand(input("Hand: "))

        avg_tricks, N, runtime = mean_tricks(trump, hand, n_players, pos, n_hands, n_repeat, time_limit=time_limit)  
        print(f'Ran {N} simulations in {runtime}s. Average tricks taken: {avg_tricks}\n\n')
        pos -= 1
        if pos < 0: pos += n_players


if __name__ == '__main__':
    n_players = int(input('Number of players: '))
    pos = int(input('Table position relative to dealer (0 for 1st, 1 for 2nd, etc.): '))
    n_hands = int(input("Number of hands simulated: "))
    n_repeat = int(input("Number of iterations for each hand: "))
    time_limit = int(input("Simulation time limit in seconds: "))

    play_game(n_players, pos, n_hands, n_repeat, time_limit=time_limit)
