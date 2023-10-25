SPACE = "/"
letter_to_morse = {'A': '.-',
                   'B': '-...',
                   'C': '-.-.',
                   'D': '-..',
                   'E': '.',
                   'F': '..-.',
                   'G': '--.',
                   'H': '....',
                   'I': '..',
                   'J': '.---',
                   'K': '-.-',
                   'L': '.-..',
                   'M': '--',
                   'N': '-.',
                   'O': '---',
                   'P': '.--.',
                   'Q': '--.-',
                   'R': '.-.',
                   'S': '...',
                   'T': '-',
                   'U': '..-',
                   'V': '...-',
                   'W': '.--',
                   'X': '-..-',
                   'Y': '-.--',
                   'Z': '--..',
                   '1': '.----',
                   '2': '..---',
                   '3': '...--',
                   '4': '....-',
                   '5': '.....',
                   '6': '-....',
                   '7': '--...',
                   '8': '---..',
                   '9': '----.',
                   '0': '-----',
                   ' ': SPACE
                   }

morse_to_letters = {value: key for key, value in letter_to_morse.items()}


def morse_to_text(text):
    encoded_text_list = text.split(" ")
    decoded_text = [morse_to_letters[code] for code in encoded_text_list]
    return ''.join(decoded_text)


def text_to_morse(text):
    encoded_text = [letter_to_morse[letter.upper()] for letter in text]
    return ' '.join(encoded_text)


action = None
while True:
    action = input("Do you want to decode or encode morse code? (Type 'encode' or 'decode'): ").lower()

    if action == "encode" or action == "decode":
        print(f"You've selected {action}")
        break
    else:
        print(f"{action} is not valid. Please select a valid action.")
        continue


text = input(f"Paste the text you want to {action}:")

if action == "encode":
    print(text_to_morse(text))
else:
    print(morse_to_text(text))



