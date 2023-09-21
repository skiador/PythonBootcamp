import pandas as pd

# TODO 1. Create a dictionary in this format:
df = pd.read_csv("nato_phonetic_alphabet.csv")

alphabet = {row.letter: row.code for index, row in df.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.


def spelling():
    word = input("Enter a word:")
    try:
        result = [alphabet[letter.upper()] for letter in word]
        print(result)
        spelling()
    except KeyError as e:
        print(f"Type only valid characters, {e} is not a valid character.")
        spelling()


spelling()