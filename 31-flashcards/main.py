import tkinter as ttk
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"

try:
    data = pd.read_csv("./data/words_to_know.csv")
except (FileNotFoundError, pd.errors.EmptyDataError):
    data = pd.read_csv("./data/french_words.csv")

to_learn = data.to_dict(orient="records")
new_card = {}


def new_flashcard():
    global new_card, flip_timer
    root.after_cancel(flip_timer)
    canvas.itemconfig(background, image=flashcard_front)
    new_card = random.choice(to_learn)
    canvas.itemconfig(language, text=list(new_card.keys())[0], fill="black")
    canvas.itemconfig(word, text=new_card["French"], fill="black")
    flip_timer = root.after(3000, flip)


def flip():
    canvas.itemconfig(background, image=flashcard_rear)
    canvas.itemconfig(language, text=list(new_card.keys())[1], fill="white")
    canvas.itemconfig(word, text=new_card["English"], fill="white")


def known_word():
    try:
        to_learn.remove(new_card)
    except (IndexError, ValueError):
        canvas.itemconfig(language, text="")
        canvas.itemconfig(word, text="You've completed all words!")
    else:
        new_flashcard()
    finally:
        data = pd.DataFrame(to_learn)
        data.to_csv("./data/words_to_know.csv", index=False)


# Setup main window
root = ttk.Tk()
root.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

# Card setup
canvas = ttk.Canvas(root, width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0)
flashcard_front = ttk.PhotoImage(file="./images/card_front.png")
flashcard_rear = ttk.PhotoImage(file="./images/card_back.png")
background = canvas.create_image((400, 263), image=flashcard_front)
canvas.grid(column=0, columnspan=2, row=0, padx=50, pady=50)
language = canvas.create_text(400, 150, text="Test", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, text="Test", font=("Ariel", 60, "bold"))

# Buttons
unknown_button_image = ttk.PhotoImage(file="./images/wrong.png")
unknown_button = ttk.Button(image=unknown_button_image, command=new_flashcard, highlightthickness=0, borderwidth=-10)
unknown_button.grid(column=0, row=1)

known_button_image = ttk.PhotoImage(file="./images/right.png")
known_button = ttk.Button(image=known_button_image, command=known_word, highlightthickness=0, borderwidth=-10)
known_button.grid(column=1, row=1)

flip_timer = root.after(3000, flip)
new_flashcard()

root.mainloop()
