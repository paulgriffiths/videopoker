'''Poker machine class.'''

import pcards

GAME_START = 1
GAME_POSTDEAL = 2
GAME_OVER = 3

class NegativeBet(Exception):

    '''Negative bet exception class.'''

    pass

class NotEnoughMoney(Exception):

    '''Not enough money exception class.'''

    pass

class PokerMachine():

    """Implements a video poker machine class."""

    def __init__(self):

        """Instance initialization function."""

        # Set up variables

        self.deck = pcards.Deck()
        self.hand = None

        self.game_easy = True

        self.game_status = GAME_START
        self.pot = 100
        self.defaultbet = 5
        self.bet = 5
        self.start_new_game()

    def flip(self, position):

        '''Flip method.'''

        self.hand.flip(position)

    def start_new_game(self):

        """Returns the game an interface to its starting point."""

        self.game_status = GAME_START
        self.pot = 100
        self.defaultbet = 5
        self.bet = 5

    def make_bet(self, amount=None):

        """Processes the player's bet and deals a new hand
        if the bet is valid.

        """

        if amount:
            self.bet = amount
        else:
            self.bet = self.defaultbet

        if self.bet > self.pot:
            raise NotEnoughMoney
        elif self.bet < 1:
            raise NegativeBet

        # We have a valid bet, so shuffle the deck
        # and get a new poker hand.

        self.deck.shuffle()
        self.hand = pcards.PokerHand(self.deck)
        self.hand.face_up()

        # Update game variables and GUI

        self.pot -= self.bet

        self.game_status = GAME_POSTDEAL

    def evaluate_hand(self):

        """Evalutes a player's hand after any exchanges have
        been made and we have the final hand. Process
        winnings if we have any.

        """

        # Player has flipped their cards if we're here,
        # so figure out which ones they flipped and
        # exchange them and show the new cards.

        xchg_str = ""

        for (flipped, position) in enumerate(self.flipped):
            if flipped:
                xchg_str += position + 1

        self.hand.exchange(xchg_str)
        self.show_cards()

        # Calculate winnings and show status

        winnings = self.hand.video_winnings(self.bet, easy=self.game_easy)

        if winnings:
            self.pot += winnings
        else:
            if self.pot == 0:
                self.game_status = GAME_OVER

        # Reset the bet amount field with the default bet. Check
        # here to make sure the default bet is not more money that
        # is in the pot, and limit it to that amount if it is.

        self.defaultbet = self.bet if self.bet <= self.pot else self.pot
        self.game_status = GAME_OVER

        # Discard and then drop the current hand

        self.hand.discard()
        self.hand = []

    def hand_string(self):

        """Shows the cards in the poker hand on the screen."""

        if self.hand:
            card_string = None
            for card in self.hand:
                if card:
                    if card.is_face_up():
                        this_card = card.name_string(True)
                    else:
                        this_card = '[Flipped]'
                else:
                    this_card = "[empty]"

                if not card_string:
                    card_string = "{0}".format(this_card)
                else:
                    card_string += ", {0}".format(this_card)
        else:
            card_string = '[No dealt hand]'

        return card_string

