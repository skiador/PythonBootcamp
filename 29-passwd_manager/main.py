import json
import time
from tkinter import *
from tkinter import messagebox, ttk
import random
import pyperclip
import string


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def gen_passwd():
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+=-[]{}|;:,.<>?/\\"
    passwd = ''.join(random.choice(characters) for _ in range(16))
    # Escape double and single quotes
    passwd = passwd.replace('"', '\\"').replace("'", "\\'")
    passwd_input.delete(0, END)
    passwd_input.insert(0, passwd)
    pyperclip.copy(passwd)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def add_info():
    website = website_input.get()
    email_user = email_user_input.get()
    passwd = passwd_input.get()

    if any(value is None or value == "" for value in [website, email_user, passwd]):
        messagebox.showwarning(title="Check details", message="Please fill all required information.")
    elif "'" in website or "'" in email_user or '"' in website or '"' in email_user:
        messagebox.showwarning(title="Check details", message="Single or double quotation marks are not permitted.")

    else:
        is_ok = messagebox.askokcancel(
            title="Confirmation",
            message=f"Are you sure you want to add the following information?"
                    f"\nWebsite: {website}"
                    f"\nEmail/Username: {email_user}"
                    f"\nPassword: {passwd}"
        )
        if is_ok:
            try:
                with open("./info.json", mode="r") as file:
                    existing_data = json.load(file)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                existing_data = {}

            if website in existing_data.keys():
                if email_user in existing_data[website].keys():
                    result = messagebox.askyesno(
                        title="Existing password",
                        message=f"The username already exists for {website}. Do you want to update the password?")
                    if result:
                        existing_data[website][email_user] = passwd
                    else:
                        messagebox.showinfo(title="Info", message="Operation canceled")
                        return
                else:
                    result = messagebox.askyesno(
                        title="Existing password",
                        message=f"You already have a password-username pair for {website}. "
                                f"Press yes to add a the new pair or no to cancel.")
                    if result:
                        existing_data[website][email_user] = passwd
                    else:
                        messagebox.showinfo(title="Info", message="Operation canceled")
                        return
            else:
                existing_data[website] = {email_user: passwd}

            with open("./info.json", "w") as file:
                json.dump(existing_data, file, indent=4)

            passwd_input.delete(0, END)
            website_input.delete(0, END)
            update_status(website)
            window.after(2000, clear_status)


def update_status(website):
    status_label.config(text=f"Info for {website} Added Successfully!")


def clear_status():
    status_label.config(text="")


# ---------------------------- PASSWD SEARCH ------------------------------- #


def search_password():
    def search_data(event):
        search_term = search_box.get().lower()
        tree.delete(*tree.get_children())
        with open("./info.json") as data:
            existing_data = json.load(data)

        for website, credentials in existing_data.items():
            for username, password in credentials.items():
                if search_term in website.lower() or search_term in username.lower():
                    # Insert matching data into the treeview
                    tree.insert("", "end", values=(website, username, password))

    def copy_password():
        selected_item = tree.selection()
        if selected_item:
            data = tree.item(selected_item)["values"]
            if data:
                website, username, password = data
                pyperclip.copy(password)
                status_label_search.config(text="Password copied to clipboard!")
                search_window.update()
                time.sleep(3)
                status_label_search.config(text="")

    search_window = Toplevel(window)
    search_window.title("Search")
    search_window.geometry("600x500")
    search_window.columnconfigure(0, weight=1)
    search_window.columnconfigure(1, weight=3)
    search_box = Entry(search_window)
    search_box.grid(column=1, row=0, padx=50, sticky="ew")
    search_box_label = Label(search_window, text="Website: ")
    search_box_label.grid(column=0, row=0, sticky="e")
    copy_passwd = Button(search_window, text="Copy Password", command=copy_password)
    copy_passwd.grid(column=0, row=5, columnspan=2)
    status_label_search = Label(search_window, text="", fg="grey")
    status_label_search.grid(column=0, row=6, columnspan=2)

    tree = ttk.Treeview(search_window, show="headings")
    tree.grid(column=0, row=1, columnspan=2, pady=20, padx=50, sticky="ew")
    tree["columns"] = ("Website", "Username", "Password")
    tree.heading("#1", text="Website")
    tree.heading("#2", text="Username")
    tree.heading("#3", text="Password")
    tree.column("#1", width=100)
    tree.column("#2", width=100)
    tree.column("#3", width=100)

    search_box.bind("<KeyRelease>", search_data)


# ---------------------------- UI SETUP ------------------------------- #

# Window and canvas setup
window = Tk()
window.title("Password Manager")
window.geometry("600x500")
window.columnconfigure(0, weight=1)  # Column 0
window.columnconfigure(1, weight=1)  # Column 1
window.columnconfigure(2, weight=1)  # Column 2
window.columnconfigure(3, weight=1)  # Column 2
canvas = Canvas(width=200, height=190)
bg_image = PhotoImage(file="logo.png")
canvas.create_image(100, 90, image=bg_image)
canvas.grid(column=0, row=0, columnspan=4, pady=10)

# Inputs setup
website_input = Entry()
website_input.grid(column=1, row=2, columnspan=2, stick="ew", pady=5, padx=25)
email_user_input = Entry()
email_user_input.grid(column=1, row=3, columnspan=2, stick="ew", pady=5, padx=25)
passwd_input = Entry()
passwd_input.grid(column=1, row=4, columnspan=1, stick="ew", pady=5, padx=25)

# Buttons
gen_passwd = Button(text="Generate Password", command=gen_passwd, borderwidth=2, relief="ridge")
gen_passwd.grid(column=2, row=4, columnspan=1, stick="ew", pady=5, padx=25)
add_passwd = Button(text="Add Password", command=add_info, borderwidth=2, relief="ridge")
add_passwd.grid(column=1, row=5, columnspan=2, stick="ew", pady=5, padx=25)
search_passwd = Button(text="Search", command=search_password, borderwidth=2, relief="ridge")
search_passwd.grid(column=0, row=1, columnspan=4, pady=50)

# Labels
website_label = Label(text="Website: ")
website_label.grid(column=0, row=2, sticky="e")
email_user_label = Label(text="Email/Username")
email_user_label.grid(column=0, row=3, sticky="e")
passwd_label = Label(text="Password")
passwd_label.grid(column=0, row=4, sticky="e")
status_label = Label(text="", fg="grey")
status_label.grid(column=1, row=6, columnspan=2)

window.mainloop()
