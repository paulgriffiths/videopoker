"""Poker hand widget."""

# Disable pylint message from inherited tkinter classes
# pylint: disable=too-many-public-methods

from tkinter import Label, Frame, TOP, LEFT, SUNKEN
import pcards

class CardPlace(Label):

    '''Card place class.'''

    def __init__(self, parent, cardImages, card=None, flipped=False):

        '''Initializes a card place.'''

        Label.__init__(self, parent)
        self.bind('<Button-1>', self.flip)
        self.cardImages = cardImages
        self.flippable = True

        self.place(card, flipped)

    def setImage(self):
        if self.card:
            if self.flipped:
                newImage = self.cardImages.back()
            else:
                newImage = self.cardImages.card(self.card.index() + 1)
        else:
            newImage = self.cardImages.empty()
        self.configure(image=newImage)

    def place(self, card=None, flipped=False):
        self.card = card
        self.flipped = flipped
        self.flippable = True
        self.setImage()

    def isEmpty(self):
        return not self.card

    def clear(self):
        oldCard = self.card
        self.place(None)
        return oldCard

    def enableFlip(status=True):
        self.flippable = status

    def flip(self, dummy):

        '''Flips a card if there is currently a card in this place.'''

        if self.flippable and self.card:
            self.flipped = not self.flipped
            self.setImage()

class HandPlace(Frame):

    '''Hand place class.'''

    def __init__(self, parent, cardImages):

        '''Initializes a hand place.'''

        Frame.__init__(self, parent)
        self.arena = Label(self, relief=SUNKEN)
        self.arena.pack(side=TOP)
        self.cards = []
        self.deck = pcards.Deck()

        for cardnum in range(5):
            newcard = CardPlace(self.arena, cardImages)
            newcard.pack(side=LEFT, padx=10, pady=10)
            self.cards.append(newcard)

    def deal(self):
        for card in self.cards:
            if not card.isEmpty():
                self.deck.discard([card.clear()])
        self.deck.shuffle(True)
        for card in self.cards:
            card.place(self.deck.draw()[0])

