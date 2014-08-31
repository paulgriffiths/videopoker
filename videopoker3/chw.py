#!/usr/bin/env python3

from tkinter import Tk, TOP, BOTTOM, Button, YES, X, Frame, SUNKEN, RAISED
from tkinter import Label, LEFT, RIGHT, Entry, END
import pcards
import cardhandwidget
import cardimages

ncards = 3
deck = pcards.Deck()
hand = pcards.Hand(deck)

def main():
    root = Tk()

    global chw
    chw = cardhandwidget.CardHandWidget(root, cardimages.CardImages,
                                        numcards=ncards, relief=SUNKEN,
                                        borderwidth=1)
    chw.pack(side=TOP, padx=5, pady=5)

    bf = Label(root, relief=SUNKEN)
    bf.pack(side=BOTTOM, expand=YES, fill=X, padx=5, pady=5)

    bff = Frame(bf)
    bff.pack(side=TOP)

    bfff = Frame(bff)
    bfff.pack(side=TOP)

    db = Button(bfff, text="Deal", command=lambda chw=chw: deal_button(chw))
    db.pack(side=LEFT, padx=5, pady=5)

    qb = Button(bfff, text="Quit", command=root.destroy)
    qb.pack(side=RIGHT, padx=5, pady=5)

    xb = Button(bfff, text="Exchange", command=exchange_button)
    xb.pack(side=RIGHT, padx=5, pady=5)

    pb = Button(bfff, text="Show", command=show_button)
    pb.pack(side=RIGHT, padx=5, pady=5)

    global sw
    sw = Label(bff, relief=SUNKEN)
    set_status_text("No text to show")
    sw.pack(side=BOTTOM, padx=5, pady=5)

    root.mainloop()

def exchange_button():
    hand.exchange(face_up=True)
    #chw.refresh()
    pass

def show_button():
    msg = chw.show_hand()
    set_status_text(msg)

def set_status_text(text):
    sw.configure(text=text)

def deal_button(chw):
    hand.discard()
    deck.shuffle()
    hand.draw(ncards, face_up=True)
    chw.deal(hand)
    print("Deck has", len(deck), "cards, discard pile has",
          deck.discard_size())

if __name__ == '__main__':
    main()

