from tkinter import *

import pandas
from pandas import *
from random import *


BACKGROUND_COLOUR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


def is_known():
    to_learn.remove(current_card)
    learn_data = pandas.DataFrame(to_learn)
    learn_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
window.config(bg=BACKGROUND_COLOUR, padx=50, pady=50)
window.title("Flashy")
flip_timer = window.after(3000, func=flip_card)

card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOUR, highlightthickness=0)
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

image_known = PhotoImage(file="images/right.png")
known_button = Button(image=image_known, highlightthickness=0, bd=0, activebackground=BACKGROUND_COLOUR,
                      command=is_known)
known_button.grid(column=1, row=1)

image_unknown = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=image_unknown, highlightthickness=0, bd=0, activebackground=BACKGROUND_COLOUR,
                        command=next_card)
unknown_button.grid(column=0, row=1)

next_card()


window.mainloop()
