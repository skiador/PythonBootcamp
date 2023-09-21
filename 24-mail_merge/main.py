with open("./Input/Names/invited_names.txt") as names_file, open("./Input/Letters/starting_letter.txt") as file:
    names = names_file.read().splitlines()
    letter = file.read()

for name in names:
    mod_letter = letter.replace("[name]", name)
    output_path = f"./Output/ReadyToSend/letter_for_{name}.txt"
    with open(output_path, mode="w") as ready_letter:
        ready_letter.write(mod_letter)


