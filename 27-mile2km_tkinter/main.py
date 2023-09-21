# import tkinter
#
# def click_button():
#     text = input.get()
#     my_label.config(text=text)
#
# window = tkinter.Tk()
# window.title("TestTitle")
# window.minsize(width=500, height=500)
#
# my_label = tkinter.Label(text="TestLabel", font=("Arial", 20, "bold"))
# my_label.pack()
#
# my_button = tkinter.Button(text="TestButton", command=click_button)
# my_button.pack()
#
# input = tkinter.Entry()
# input.pack()
#
#
# window.mainloop()
#


from tkinter import *


def calculate_m2km(event=None):
    miles = float(input_value.get())
    km = round(miles * 1.609344, 2)
    result.config(text=km)


def calculate_km2m(event=None):
    km = float(input_value.get())
    miles = round(km / 1.609344, 2)
    result.config(text=miles)


# Window settings
window = Tk()
window.title("Miles-Kilometers Converter")
window.minsize(width=200, height=50)
window.config(padx=20, pady=20)


# Miles input
input_value = Entry(width=10)
input_value.grid(column=1, row=0)
input_value.focus()
input_value.insert(0, string="0")


# Labels
initial_unit = Label(text="Miles")
initial_unit.grid(column=2, row=0)
is_equal_to = Label(text="is equal to")
is_equal_to.grid(column=0, row=1)
result = Label(text="0")
result.grid(column=1, row=1)
final_unit = Label(text="Km")
final_unit.grid(column=2, row=1)


# Button
calculate = Button(text="Calculate", command=calculate_m2km)


# Mode selection
previous_value = 1


def radio_used():
    global previous_value
    current_value = radio_state.get()
    if current_value != previous_value:  # Check if the value has changed
        if radio_state.get() == 1:
            initial_unit.config(text="Miles")
            final_unit.config(text="Km")
            calculate.config(command=calculate_m2km)
            input_value.delete(0, END)
            input_value.insert(0, result.cget("text"))
            calculate.invoke()

        elif radio_state.get() == 2:
            initial_unit.config(text="Km")
            final_unit.config(text="Miles")
            calculate.config(command=calculate_km2m)
            input_value.delete(0, END)
            input_value.insert(0, result.cget("text"))
            calculate.invoke()
    previous_value = current_value


# Variable to hold on to which radio button value is checked.
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Miles to Km", value=1, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Km to Miles", value=2, variable=radio_state, command=radio_used)
radiobutton1.grid(column=3, row=0)
radiobutton2.grid(column=3, row=1)
radiobutton1.config(padx=50)
radiobutton2.config(padx=50)
radio_state.set(2)
radio_used()
calculate_m2km()


# Bind the calculate functions to the input field
input_value.bind("<KeyRelease>", calculate_m2km)
input_value.bind("<KeyRelease>", calculate_km2m)

window.mainloop()
