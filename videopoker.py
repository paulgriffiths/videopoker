#!/usr/bin/python

"""A video poker game using the Tkinter library.

Release 1.1

Copyright 2013 Paul Griffiths
Email: mail@paulgriffiths.net

Distributed under the terms of the GNU General Public License.
http://www.gnu.org/licenses/
"""

# Disable the following pylint messages:
#  - Too many instance attributes, potential future refactor
#
# pylint: disable=R0902


from Tkinter import Tk, Menu, Label, Button, Entry, sys, PhotoImage
from Tkinter import N, E, S, W, SUNKEN, RAISED, NORMAL, DISABLED
from Tkinter import StringVar, Toplevel, mainloop
import tkMessageBox

import pcards


class PokerMachine():

    """Implements a video poker machine class."""

    def __init__(self):

        """Instance initialization function."""

        # Set up variables

        self.deck = pcards.Deck()
        self.cardimg = []
        self.hand = None

        self.game_start = True
        self.game_postdeal = False
        self.game_easy = True
        self.game_over = False
        self.gifdir = "./images/"

        self.pot = 100
        self.defaultbet = 5
        self.bet = 5

        self._set_up_gui()

    def button_clicked(self):

        """Event handler for button click.

        Callback method called by tk.

        """

        if self.game_over:
            self._start_new_game()
        elif not self.game_postdeal:
            self._process_bet()
        elif self.game_postdeal:
            self._evaluate_hand()

    def flip(self, event):

        """Event handler which flips a clicked card.

        Callback method called by tk.

        """

        if not self.game_postdeal:
            return

        if event.widget.flipped:
            event.widget.flipped = False
            event.widget.configure(image=event.widget.cardimage)
        else:
            event.widget.flipped = True
            event.widget.configure(image=self.backimg)

    def _start_new_game(self):

        """Returns the game an interface to its starting point."""

        for cardimg in self.cardimg:
            cardimg.configure(image=self.backimg)
            cardimg.flipped = True

        self.game_over = False
        self.game_postdeal = False
        self.pot = 100
        self.defaultbet = 5
        self.bet = 5
        self._update_pot()
        self.bet_amt_fld.configure(state=NORMAL)
        self.bet_str.set(str(self.defaultbet))
        self.button.configure(text="Deal")
        self.status_lbl.configure(text="Click 'Deal' to play.")

    def _process_bet(self):

        """Processes the player's bet and deals a new hand
        if the bet is valid.

        """

        # First check if played made a valid bet,
        # and return with no change in state (other
        # than resetting the bet field) if they did
        # not.

        b_str = self.bet_str.get()

        try:
            self.bet = int(b_str)
        except ValueError:
            self._show_bet_error("Bad bet!", "You must bet a whole number!")
            return

        if self.bet > self.pot:
            self._show_bet_error("Don't be greedy!",
                                 "You don't have that much money!")
            return
        elif self.bet < 1:
            self._show_bet_error("Don't get clever!",
                                 "You must bet a positive whole number!")
            return

        # We have a valid bet, so shuffle the deck
        # and get a new poker hand.

        self.deck.shuffle()
        self.hand = pcards.PokerHand(self.deck)
        self._show_cards()

        # Update game variables and GUI

        self.pot -= self.bet
        self._update_pot()

        self.button.configure(text="Exchange / skip")
        self.status_lbl.configure(text="Choose cards to exchange by " +
                                       "clicking on them.")
        self.bet_amt_fld.configure(state=DISABLED)

        self.game_postdeal = True

    def _evaluate_hand(self):

        """Evalutes a player's hand after any exchanges have
        been made and we have the final hand. Process
        winnings if we have any.

        """

        # Player has flipped their cards if we're here,
        # so figure out which ones they flipped and
        # exchange them and show the new cards.

        xchg_str = ""

        for cardimg in self.cardimg:
            if cardimg.flipped:
                xchg_str += cardimg.pos

        self.hand.exchange(xchg_str)
        self._show_cards()

        # Calculate winnings and show status

        winnings = self.hand.video_winnings(self.bet, easy=self.game_easy)
        win_str = self.hand.show_value() + ". "

        if winnings:
            self.pot += winnings
            win_str += "You won ${0:}!".format(winnings)
            self._update_pot()
        else:
            win_str += "Sorry, no win!"
            if self.pot == 0:
                win_str += " Out of money - game over!"
                self.game_over = True

        self.status_lbl.configure(text=win_str)

        # Update game variables and GUI

        if self.game_over:
            self.button.configure(text="New game")
        else:
            self.button.configure(text="Deal again")
            self.bet_amt_fld.configure(state=NORMAL)

        # Reset the bet amount field with the default bet. Check
        # here to make sure the default bet is not more money that
        # is in the pot, and limit it to that amount if it is.

        self.defaultbet = self.bet if self.bet <= self.pot else self.pot
        self.bet_str.set(str(self.defaultbet))
        self.game_postdeal = False

        # Discard and then drop the current hand

        self.hand.discard()
        self.hand = []

    def _show_bet_error(self, title, message):

        """Shows a message box and resets the bet field
        in response to an invalid bet.

        """

        tkMessageBox.showerror(title, message)
        self.bet = self.defaultbet
        self.bet_str.set(str(self.defaultbet))

    def _update_pot(self):

        """Updates the pot amount label with the current pot."""

        txt_str = "${0:}".format(self.pot)
        self.pot_amt_lbl.configure(text=txt_str)

    def _show_cards(self):

        """Shows the cards in the poker hand on the screen."""

        for cardimg, idx in zip(self.cardimg, self.hand.index_list()):
            cardfile = "{0}{1}.gif".format(self.gifdir, str(idx + 1))
            img = PhotoImage(file=cardfile)
            cardimg.configure(image=img)
            cardimg.cardimage = img
            cardimg.flipped = False

    def _set_up_gui(self):

        """Sets up the Tkinter user interface."""

        # Disable pylint warning for instance attributes defined outside
        # __init__(), since this method is called by __init__()
        #
        # pylint: disable=W0201

        self.root = Tk()
        self.root.title('Video Poker')

        # Set up menubar

        self.menubar = Menu(self.root)

        self.gamemenu = Menu(self.menubar, tearoff=0)
        self.gamemenu.add_command(label="Quit", command=sys.exit)
        self.menubar.add_cascade(label="Game", menu=self.gamemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="About", command=self.help_about)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.root.config(menu=self.menubar)

        # Set up card images

        self.backimg = PhotoImage(file="{0}b.gif".format(self.gifdir))

        for num in range(5):
            lbl = Label(self.root, image=self.backimg)
            lbl.grid(row=0, column=num, padx=10, pady=10)
            lbl.bind("<Button-1>", self.flip)
            lbl.flipped = True
            lbl.pos = str(num + 1)
            self.cardimg.append(lbl)

        # Set up labels, fields and buttons

        self.pot_lbl = Label(self.root, text="Pot:")
        self.pot_lbl.grid(row=1, column=0,
                          padx=10, pady=2, sticky=W)

        self.pot_amt_lbl = Label(self.root, text="")
        self.pot_amt_lbl.grid(row=1, column=1, columnspan=2,
                              padx=10, pady=2, sticky=W)
        self._update_pot()

        self.bet_lbl = Label(self.root, text="Bet ($):")
        self.bet_lbl.grid(row=2, column=0,
                          padx=10, pady=2, sticky=W)

        self.bet_str = StringVar()
        self.bet_str.set(str(self.defaultbet))

        self.bet_amt_fld = Entry(self.root, textvariable=self.bet_str)
        self.bet_amt_fld.grid(row=2, column=1, columnspan=2,
                              padx=10, pady=2, sticky=W)

        self.button = Button(self.root, text="Deal",
                             command=self.button_clicked)
        self.button.grid(row=1, column=3, rowspan=2, columnspan=2,
                         sticky=W + E + S + N, padx=10)

        self.status_lbl = Label(self.root, bd=1, relief=SUNKEN,
                                text="Welcome to the casino! " +
                                     "Click 'Deal' to play!")
        self.status_lbl.grid(row=3, column=0, columnspan=5,
                             padx=10, pady=10, ipadx=10, ipady=10,
                             sticky=W + E + S + N)

        # Show winnings table

        lbl = Label(self.root, text="Winnings Table", relief=RAISED)
        lbl.grid(row=4, column=1, columnspan=3,
                 pady=15, ipadx=10, ipady=10, sticky=W + E)

        # Two different tables, one for easy mode, one for normal
        # mode, so be prepared to show either one.

        wte = {2500: "Royal Flush", 250: "Straight Flush",
               100: "Four of a Kind", 50: "Full House", 20: "Flush",
               15: "Straight", 4: "Three of a Kind", 3: "Two Pair",
               2: "Jacks or Higher"}
        wtn = {800: "Royal Flush", 50: "Straight Flush", 25: "Four of a Kind",
               9: "Full House", 6: "Flush", 4: "Straight",
               3: "Three of a Kind", 2: "Two Pair", 1: "Jacks or Higher"}
        wtxt = wte if self.game_easy else wtn

        row = 5
        for key in sorted(wtxt.keys(), reverse=True):
            lbl = Label(self.root, text=wtxt[key])
            lbl.grid(row=row, column=1, columnspan=2, sticky=W)
            lbl = Label(self.root, text="{0} : 1".format(key))
            lbl.grid(row=row, column=3, sticky=E)
            row += 1

        lbl = Label(self.root, text="")
        lbl.grid(row=row, column=0, columnspan=5, pady=15)

        # pylint: enable=W0201

    def help_about(self):

        """Shows an 'about' modal dialog.

        Callback method called by tk.

        """

        about_win = Toplevel(self.root)

        # Set up dialog

        lbl = Label(about_win, text="Video Poker")
        lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky=W + N)
        lbl = Label(about_win, text="by Paul Griffiths")
        lbl.grid(row=1, column=0, padx=10, pady=(0, 7), sticky=W + N)
        lbl = Label(about_win, text="Written in Python, with tkinter.")
        lbl.grid(row=2, column=0, padx=10, pady=7, sticky=W + N)
        lbl = Label(about_win, text="Copyright 2013 Paul Griffiths")
        lbl.grid(row=4, column=0, padx=10, pady=(7, 0), sticky=W + N)
        lbl = Label(about_win, text="Email: mail@paulgriffiths.net")
        lbl.grid(row=5, column=0, padx=10, pady=(0, 21), sticky=W + N)
        lbl = Label(about_win, text="This program is free software: you can " +
            "redistribute it and/or modify it under the terms")
        lbl.grid(row=6, column=0, columnspan=2,
                 padx=10, pady=0, sticky=W + N)
        lbl = Label(about_win, text="of the GNU General Public License as " +
            "published by the Free Software Foundation, either")
        lbl.grid(row=7, column=0, columnspan=2,
                 padx=10, pady=(0, 0), sticky=W + N)
        lbl = Label(about_win, text="version 3 of the License, or " +
            "(at your option) any later version.")
        lbl.grid(row=8, column=0, columnspan=2,
                 padx=10, pady=(0, 21), sticky=W + N)
        lbl = Label(about_win, text="This program is distributed in " +
            "the hope that it will be useful, but WITHOUT ANY WARRANTY;")
        lbl.grid(row=9, column=0, columnspan=2,
                 padx=10, pady=0, sticky=W + N)
        lbl = Label(about_win, text="without even the implied " +
            "warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR")
        lbl.grid(row=10, column=0, columnspan=2,
                 padx=10, pady=(0, 0), sticky=W + N)
        lbl = Label(about_win, text="PURPOSE. See the " +
            "GNU General Public License for more details.")
        lbl.grid(row=11, column=0, columnspan=2,
                 padx=10, pady=(0, 21), sticky=W + N)
        lbl = Label(about_win, text="You should have received a " +
            "copy of the GNU General Public License along with this")
        lbl.grid(row=12, column=0, columnspan=2,
                 padx=10, pady=(0, 0), sticky=W + N)
        lbl = Label(about_win, text="program. If not, see " +
            "<http://www.gnu.org/licenses/>.")
        lbl.grid(row=13, column=0, columnspan=2,
                 padx=10, pady=(0, 21), sticky=W + N)
        img = PhotoImage(file="{0}27.gif".format(self.gifdir))
        lbl = Label(about_win, image=img)
        lbl.grid(row=0, column=1, rowspan=5, padx=10, pady=10, sticky=N + E)

        btn = Button(about_win, text="OK", command=about_win.quit)
        btn.grid(row=14, column=0, columnspan=2,
                 padx=0, pady=(0, 10), ipadx=30, ipady=3)

        # Show dialog

        about_win.transient(self.root)
        about_win.parent = self.root
        about_win.protocol("WM_DELETE_WINDOW", about_win.destroy)
        about_win.geometry("+{0}+{1}".format(self.root.winfo_rootx() + 50,
                                           self.root.winfo_rooty() + 50))
        about_win.title("About Video Poker")
        about_win.focus_set()
        about_win.grab_set()
        about_win.mainloop()
        about_win.destroy()


# Entry point to main() function

if __name__ == '__main__':
    PM = PokerMachine()
    mainloop()
