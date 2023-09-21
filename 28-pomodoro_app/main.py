from tkinter import *


# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer = ""
# ---------------------------- TIMER RESET ------------------------------- # 


def reset():
    global reps
    window.after_cancel(timer)
    reps = 0
    ticks.config(text="")
    work.config(text="")
    canvas.itemconfig(timer_text, text=f"00:00")

# ---------------------------- TIMER MECHANISM ------------------------------- # 


def start_timer():
    global reps
    reps += 1
    if reps % 8 == 0:
        work.config(text="BREAK", foreground=RED)
        countdown(LONG_BREAK_MIN * 60)
    elif reps % 2 == 0:
        work.config(text="BREAK", foreground=PINK)
        countdown(SHORT_BREAK_MIN * 60)
    else:
        work.config(text="WORK", foreground=GREEN)
        countdown(WORK_MIN * 60)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def countdown(count):
    global timer
    minutes = count // 60
    seconds = count % 60
    if count > 0:
        canvas.itemconfig(timer_text, text=f"{minutes}:{seconds:02}")
        timer = window.after(1, countdown, count - 1)
    else:
        start_timer()
        if reps % 2 == 0:
            ticks.config(text=ticks.cget("text") + "\u2713")
        if reps % 8 == 0:
            ticks.config(text=ticks.cget("text") + "\u007C")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(pady=50, padx=50, bg=YELLOW)
canvas = Canvas(width=200, height=224, highlightthickness=0, bg=YELLOW)
tomato = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato)
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Start button
start_button = Button(text="Start", command=start_timer)
start_button.grid(column=0, row=2)

# Reset button
reset_button = Button(text="Reset", command=reset)
reset_button.grid(column=2, row=2)

# Text labels
ticks = Label(text="", font=(FONT_NAME, 20, "bold"), bg=YELLOW, foreground=GREEN)
work = Label(text="", font=(FONT_NAME, 40, "bold"), bg=YELLOW, foreground=GREEN)
ticks.grid(column=1, row=3)
work.grid(column=1, row=0)


window.mainloop()
