import random
import numpy as np
from math import floor

table_count = 0
player_cards = []
ai_1_cards = []
ai_2_cards = []
dealer_cards = []
stack = []

threshold_to_play = 8
number_of_rounds_played = 0

win_amount = 0
lose_amount = 0

player_money = 10000
minimum_bet = 10

dealer_score = 0
player_score = 0

decks_amount = int(input("Enter number of decks to use: "))
lower_threshold = int(input("Enter lowest threshold: "))
upper_threshold = int(input("Enter highest threshold: "))
number_of_rounds = int(input("Enter number of rounds you would like to play: "))


def true_count():
    """Finds the true count on the table."""
    global table_count
    global decks_amount
    global stack

    decks_left = len(stack)/52
    count = floor(table_count/decks_left)

    return count


def build_decks(num_of_decks):
    """Constructs a given amount of decks of cards and shuffles it all."""
    global table_count

    table_count = 0

    decks = []

    for i in range(num_of_decks * 4):

        for j in range(2, 9):
            decks.append(j)

        for k in range(4):
            decks.append(10)

        decks.append(11)

    random.shuffle(decks)

    return decks


def update_table_count(card):
    """Updates the count on the table."""
    global table_count

    if card < 7:
        table_count += 1

    if card > 9:
        table_count -= 1


def draw_card():
    """Draws a single card, and updates the table count."""
    global stack

    card = stack.pop(0)
    update_table_count(card)

    return card


def deal_cards():
    """Deals a card to every player."""
    global player_cards
    global dealer_cards
    global ai_1_cards
    global ai_2_cards
    global stack

    for deal in range(2):
        ai_1_cards.append(draw_card())
        player_cards.append(draw_card())
        ai_2_cards.append(draw_card())
        dealer_cards.append(draw_card())


def clear_cards():
    """Clears the table"""
    global player_cards
    global dealer_cards
    global ai_1_cards
    global ai_2_cards

    player_cards = []
    ai_1_cards = []
    ai_2_cards = []
    dealer_cards = []


def ai_play(player):
    """Pass in 'ai 1' or 'ai 2' to play their move."""
    global ai_1_cards
    global ai_2_cards
    global dealer_cards

    hand = []

    if player == "ai 1":
        hand = ai_1_cards

    elif player == "ai 2":
        hand = ai_2_cards

    score = sum(hand)

    if dealer_cards[0] > 7:

        while score < 17:
            hand.append(draw_card())

            hand = check_for_ace(hand)

            score = sum(hand)

    else:
        while score < dealer_cards[0] + 10:
            hand.append(draw_card())

            hand = check_for_ace(hand)

            score = sum(hand)


def dealer_play():
    """Plays the dealer's hand."""
    global dealer_cards

    score = sum(dealer_cards)
    # print(f"Dealer's turn! Dealer has {dealer_cards} and a score of {score}")

    while score < 17:
        dealer_cards.append(draw_card())
        # print(f"Dealer's hits. Dealer has {dealer_cards} and a score of {score}")

        dealer_cards = check_for_ace(dealer_cards)

        score = sum(dealer_cards)
        # print(f"Dealer sticks with {dealer_cards} and a score of {score}")

    return score


def player_play(hand):
    """Plays the player's hand."""
    global dealer_cards
    global table_count

    score = sum(hand)
    # print(f"Start of hand\n-----------------------\nYou have {hand} and dealer's card is {dealer_cards[0]}")

    if dealer_cards[0] >= 7:
        while score < 17:
            hand.append(draw_card())
            score = sum(hand)
            # print(f"Hand is now {hand} and your score is {score}")

            hand = check_for_ace(hand)

            score = sum(hand)

    if 2 <= dealer_cards[0] <= 6:
        while score < 12:
            hand.append(draw_card())
            # print(f"Hand is now {hand} and your score is {score}")
            hand = check_for_ace(hand)

            score = sum(hand)

    # print(f"You stick with a score of {score}!")

    return score


def check_winner(hand, player, dealer, bet):
    """Checks for winner between player and dealer, and updates the overall score and chip total."""

    result = "draw"

    blackjack = False

    winnings = 0
    win = False
    loss = False

    if sum(hand) == 21 and len(hand) == 2:
        winnings += bet*(3/2)
        blackjack = True
        result = "win"
        win = True

    elif player > 21:
        winnings -= bet
        result = "loss"
        loss = True

    elif dealer > 21:
        winnings += bet
        result = "win"
        win = True

    elif player > dealer:
        winnings += bet
        result = "win"
        win = True

    elif player < dealer:
        winnings -= bet
        result = "loss"
        loss = True

    output = (result, winnings, win, loss, blackjack)

    return output


def check_for_ace(hand):
    """If a hand goes over 21, this checks if there is an ace in the hand and changes its value to 1."""

    while sum(hand) > 21 and 11 in hand:
        hand.sort(reverse=True)
        hand[0] = 1

    return hand


def run_game(runtime, decks, threshold):
    global player_money
    global stack

    stack = build_decks(decks)

    game_money = player_money

    wins = 0
    losses = 0
    rounds_played_in = 0
    blackjacks = 0
    blackjack_winnings = 0

    for i in range(runtime):

        p_score = 0
        p_score_1 = 0
        p_score_2 = 0

        if true_count() >= 1:
            amount_bet = (game_money / 1000) * (true_count() - 1)
        else:
            amount_bet = game_money / 1000

        deal_cards()

        if sum(player_cards) == 11 and dealer_cards[0] != 11:
            amount_bet *= 2

        if sum(player_cards) == 10 and dealer_cards[0] < 10:
            amount_bet *= 2

        ai_play("ai 1")
        ai_play("ai 2")
        if true_count() >= threshold:
            if player_cards[0] == player_cards[1] == 11 or player_cards[0] == player_cards[1] == [8]:
                new_hand_1 = [player_cards[0]]
                new_hand_2 = [player_cards[1]]
                p_score_1 = player_play(new_hand_1)
                p_score_2 = player_play(new_hand_2)

            else:
                p_score = player_play(player_cards)
        d_score = dealer_play()

        if p_score:
            result, winnings, win, loss, blackjack = check_winner(player_cards, p_score, d_score, amount_bet)
            game_money += winnings
            if win:
                wins += 1

            if loss:
                losses += 1

            if blackjack:
                blackjacks += 1
                blackjack_winnings += winnings

            rounds_played_in += 1

        if p_score_1:
            result, winnings, win, loss, blackjack = check_winner(new_hand_1, p_score_1, d_score, amount_bet)
            game_money += winnings
            if win:
                wins += 1

            if loss:
                losses += 1

            rounds_played_in += 1

        if p_score_2:
            result, winnings, win, loss, blackjack = check_winner(new_hand_2, p_score_1, d_score, amount_bet)
            game_money += winnings
            if win:
                wins += 1

            if loss:
                losses += 1

        clear_cards()

        if len(stack) < 20:
            stack = build_decks(decks)

    output = (rounds_played_in, game_money, wins, losses, blackjacks, blackjack_winnings)

    return output


for i in range(lower_threshold, upper_threshold + 1):

    rounds_list = []
    money_list = []
    wins_list = []
    losses_list = []
    blackjacks_list = []
    blackjack_winnings_list = []
    for j in range(10):

        rounds_played_in, money, wins, losses, blackjacks, blackjack_winnings = run_game(number_of_rounds, decks_amount, i)

        rounds_list.append(rounds_played_in)
        money_list.append(money)
        wins_list.append(wins)
        losses_list.append(losses)
        blackjacks_list.append(blackjacks)
        blackjack_winnings_list.append(blackjack_winnings)

    if sum(rounds_list) > 0:
        rounds_av = np.mean(rounds_list)
        money_av = round(np.mean(money_list))
        wins_av = np.mean(wins_list)
        losses_av = np.mean(losses_list)
        blackjacks_av = np.mean(blackjacks_list)
        blackjack_winnings_av = round(np.mean(blackjack_winnings_list), 1)
        av_won_per_round = round((money_av - player_money)/rounds_av, 2)
        av_bj_per_round = round(blackjacks_av/rounds_av, 3)
        win_percent = round((wins_av/rounds_av)*100, 2)
        print(
            f"Min true count: {i}. Averaged {rounds_av} rounds, {wins_av} wins, {losses_av} loses, {money_av - player_money} chips made. {av_bj_per_round} blackjacks/round with {blackjack_winnings_av} made. Win rate: {win_percent}%. Average win per round played: {av_won_per_round}")
    else:
        print(f"Min true count: {i}. Error: No rounds played.")