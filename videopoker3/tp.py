#!/usr/bin/env python3

import pokermachine

def show_money(pm):
    print("You have: ${0}".format(pm.pot))

def show_money_and_bet(pm):
    print("You have: ${0}".format(pm.pot))
    print("The current bet is: ${0}".format(pm.bet))

def show_hand(pm):
    hand_string = pm.hand_string()
    print("The current hand is: {0}".format(hand_string))

def get_bet(pm):
    show_money(pm)
    valid_bet = False
    while not valid_bet:
        bet = input("Enter your bet: ")
        if bet == "":
            pm.make_bet()
            valid_bet = True
            continue
        else:
            try:
                bet_amount = int(bet)
            except:
                print("You must bet a whole number! Try again.")
                continue

        try:
            pm.make_bet(bet_amount)
            valid_bet = True
        except pokermachine.NegativeBet:
            print("You cannot bet a negative amount! Try again.")
        except pokermachine.NotEnoughMoney:
            print("You don't have that much money! Try again.")

def flip_cards(pm):
    keep_flipping = True
    while keep_flipping:
        bad_entry = True
        while bad_entry:
            flip_string = input("Pick cards to flip: ")
            flip_list = list(flip_string)
            flip_set = set(flip_list)
            if len(flip_list) != len(flip_set):
                print("Duplicates are not allowed! Try again.")
                continue

            bad_chars = False
            for char in flip_list:
                if char not in ['1', '2', '3', '4', '5']:
                    print("Invalid entry: '{0}'".format(char))
                    bad_chars = True

            if bad_chars:
                continue

            bad_entry = False

        if not flip_list:
            print("Done flipping")
            keep_flipping = False
        else:
            print("Flipping {0}...".format(flip_string))
            for pos in flip_list:
                pm.flip(int(pos))
        show_hand(pm)



def main():
    print("Welcome to Video Poker!")
    pm = pokermachine.PokerMachine()

    keep_going = True

    while keep_going:
        print("Starting a new game...")
        pm.start_new_game()

        get_bet(pm)
        show_money_and_bet(pm)
        show_hand(pm)

        flip_cards(pm)

        keep_going = False


if __name__ == '__main__':
    main()

