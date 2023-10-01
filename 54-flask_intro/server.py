from flask import Flask
import random
app = Flask(__name__)

random_number = random.randint(0,9)
@app.route("/")
def hello_world():
    return ('<h1>Guess a number between 0 and 9</h1>'
            '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif"'
            '<p></p>')


@app.route("/<int:number>")
def check_number(number):
    if number < random_number:
        return ('<h1 style= "color: red">Too Low!</h1>'
                '<img src="https://media.giphy.com/media/D7knpKzFbgDPBmdrVM/giphy.gif"'
                '<p></p>')
    elif number > random_number:
        return ('<h1 style= "color: red">Too High!</h1>'
                '<img src="https://media.giphy.com/media/D7knpKzFbgDPBmdrVM/giphy.gif"'
                '<p></p>')
    else:
        return ('<h1 style= "color: red">Noice</h1>'
                '<img src="https://media.giphy.com/media/yJFeycRK2DB4c/giphy.gif"'
                '<p></p>')

