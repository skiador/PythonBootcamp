import pandas as pd
import turtle

# Screen setup
screen = turtle.Screen()
screen.title("U.S States Game")
image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)

# Import states info
data = pd.read_csv("50_states.csv")
states_guessed = []

while len(states_guessed) < 50:
    guess = turtle.textinput(title=f"States correct: {len(states_guessed)}/{len(data)}",
                             prompt="Type in another state name:")
    if guess is None:
        break
    elif guess.title() in data.state.to_list():
        if guess.title() in states_guessed:
            print("You already said it!")
        else:
            states_guessed.append(guess.title())
            new_guess = turtle.Turtle()
            new_guess.penup()
            new_guess.speed(0)
            new_guess.hideturtle()
            state_data = data[guess.title() == data.state]
            new_guess.goto(int(state_data.x), int(state_data.y))
            new_guess.write(f"{guess.title()}", align="center", font=("Courier", 10, "normal"))


missed_states = [state for state in data.state.to_list() if state not in states_guessed]

pd.DataFrame(missed_states).to_csv("missed_states.csv")