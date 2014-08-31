#!/usr/bin/env python3

'''Main program for Python 3 Video Poker.'''

# Disable pylint message from inherited tkinter classes
# pylint: disable=too-many-public-methods

from tkinter import Tk, Frame, Button, Label
from tkinter import TOP, BOTTOM, LEFT, RIGHT
from tkinter import SUNKEN
import pcards
import cardhandwidget
import cardimages


class ControlWidget(Frame):

    '''Control widget class.'''

    def __init__(self, parent, handler):

        '''Initialization method.'''

        Frame.__init__(self, parent)

        button_frame = Frame(self)
        button_frame.pack(side=TOP)

        self.deal_button = Button(button_frame, text="Deal",
                                  command=lambda: handler("deal"))
        self.deal_button.pack(side=LEFT, padx=5, pady=5)

        self.quit_button = Button(button_frame, text="Quit",
                                  command=lambda: handler("quit"))
        self.quit_button.pack(side=RIGHT, padx=5, pady=5)

        self.exchange_button = Button(button_frame, text="Exchange",
                                      command=lambda: handler("exchange"))
        self.exchange_button.pack(side=RIGHT, padx=5, pady=5)

        self.show_button = Button(button_frame, text="Show",
                                  command=lambda: handler("show"))
        self.show_button.pack(side=RIGHT, padx=5, pady=5)

        label_frame = Frame(self)
        label_frame.pack(side=BOTTOM)

        self.status_label = Label(label_frame, relief=SUNKEN)
        self.set_status_text("No text to show")
        self.status_label.pack(side=TOP, padx=5, pady=5)

    def set_status_text(self, text):

        '''Sets the text of the status label.'''

        self.status_label.configure(text=text)


class GameWindow(Frame):

    '''Main game window class.'''

    def __init__(self, parent):

        '''Initialization method.'''

        Frame.__init__(self, parent)

        self.deck = pcards.Deck()
        self.hand = pcards.Hand(self.deck)
        self.num_cards = 3
        self.parent = parent

        self.chw = cardhandwidget.CardHandWidget(self, cardimages.CardImages,
                                                 numcards=self.num_cards,
                                                 relief=SUNKEN, borderwidth=2)
        self.chw.pack(side=TOP, padx=5, pady=5)

        self.control_frame = ControlWidget(self, self.handler)
        self.control_frame.pack(side=BOTTOM, padx=5, pady=5)

    def handler(self, text):

        '''Handler function for ControlWidget actions.'''

        if text == 'deal':
            self.deal()
        elif text == 'exchange':
            self.exchange()
        elif text == 'quit':
            self.parent.quit()
        elif text == 'show':
            self.show()
        else:
            raise NotImplementedError

    def exchange(self):

        '''Handler for exchange action.'''

        self.hand.exchange(face_up=True)

    def show(self):

        '''Handler for show action.'''

        self.control_frame.set_status_text(self.chw.show_hand())

    def deal(self):

        '''Handler for deal action.'''

        self.hand.discard()
        self.deck.shuffle()
        self.hand.draw(self.num_cards, face_up=True)
        self.chw.deal(self.hand)


def main():

    '''Main function.'''

    root = Tk()

    game_window = GameWindow(root)
    game_window.pack(side=TOP)

    root.mainloop()

if __name__ == '__main__':
    main()
