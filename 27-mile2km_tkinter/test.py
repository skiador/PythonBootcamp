import tkinter as tk
from tkinter import ttk

def calculate_m2km(event=None):
    try:
        miles = float(input.get())
        km = round(miles * 1.609344, 2)
        result.config(text=f"{km} Km")
    except ValueError:
        result.config(text="Invalid input")

def calculate_km2m(event=None):
    try:
        km = float(input.get())
        miles = round(km / 1.609344, 2)
        result.config(text=f"{miles} Miles")
    except ValueError:
        result.config(text="Invalid input")

# Create the main window
window = tk.Tk()
window.title("Miles-Kilometers Converter")
window.geometry("400x200")
window.configure(bg="#f0f0f0")

# Style for the Labels and Entry Widgets
style = ttk.Style()
style.configure("TLabel", background="#f0f0f0", font=("Arial", 12))
style.configure("TEntry", font=("Arial", 12))

# Create and place the widgets using the grid layout
input_label = ttk.Label(window, text="Enter Distance:", style="TLabel")
input_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

input = ttk.Entry(window, width=10, style="TEntry")
input.grid(column=1, row=0, padx=10, pady=10, sticky="ew")

result_label = ttk.Label(window, text="Result:", style="TLabel")
result_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

result = ttk.Label(window, text="0 Km", style="TLabel")
result.grid(column=1, row=1, padx=10, pady=10, sticky="w")

convert_button = ttk.Button(window, text="Convert", command=calculate_m2km)
convert_button.grid(column=1, row=2, padx=10, pady=10)

# Mode selection
def radio_used():
    if radio_state.get() == 1:
        input_label.config(text="Enter Miles:")
        result_label.config(text="Result (Km):")
        convert_button.config(command=calculate_m2km)
        input.delete(0, tk.END)
        input.insert(0, result.cget("text"))
        calculate_m2km()
    elif radio_state.get() == 2:
        input_label.config(text="Enter Km:")
        result_label.config(text="Result (Miles):")
        convert_button.config(command=calculate_km2m)
        input.delete(0, tk.END)
        input.insert(0, result.cget("text"))
        calculate_km2m()

# Variable to hold which radio button value is checked
radio_state = tk.IntVar()
radio_state.set(1)  # Default to Miles to Km
radiobutton1 = ttk.Radiobutton(window, text="Miles to Km", value=1, variable=radio_state, command=radio_used)
radiobutton2 = ttk.Radiobutton(window, text="Km to Miles", value=2, variable=radio_state, command=radio_used)

radiobutton1.grid(column=0, row=2, padx=10, pady=10, sticky="w")
radiobutton2.grid(column=0, row=3, padx=10, pady=10, sticky="w")

# Bind the calculate functions to the input field
input.bind("<KeyRelease>", calculate_m2km)
input.bind("<KeyRelease>", calculate_km2m)

window.mainloop()
