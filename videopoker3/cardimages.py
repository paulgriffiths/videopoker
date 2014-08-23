"""Card images class."""

from tkinter import PhotoImage

class CardImages:

    '''Card images class.'''

    cardimgs = None
    backimg = None
    emptyimg = None
    imgdir = "images/"

    def __init__(self):

        '''This class is not intended to be instantiated.'''

        pass

    @classmethod
    def empty(cls):

        '''Returns an image for an empty card place.'''

        if not cls.emptyimg:
            cls.emptyimg = PhotoImage(file="{0}empty.gif".format(cls.imgdir))
        return cls.emptyimg

    @classmethod
    def back(cls):

        '''Returns an image for the card back.'''

        if not cls.backimg:
            cls.backimg = PhotoImage(file="{0}b.gif".format(cls.imgdir))
        return cls.backimg

    @classmethod
    def card(cls, cardindex=None):

        '''Returns a card image.'''

        if not cls.cardimgs:
            cls.cardimgs = []
            for idx in range(1, 53):
                newcard = PhotoImage(file="{0}{1}.gif".format(cls.imgdir, idx))
                cls.cardimgs.append(newcard)

        return cls.cardimgs[cardindex - 1]

