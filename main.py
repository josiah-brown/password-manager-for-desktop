from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json
import sqlite3 as sql

# ---------------------------- DATABASE ------------------------------- #
conn = sql.connect('data.db')
cursor = conn.cursor()

# Only run this once to initialize the table
# command = "CREATE TABLE info (website text, email text, password text)"
# cursor.execute(command)
# conn.commit()

# ---------------------------- CONSTANTS ------------------------------- #
# FILE_PATH = "data.txt"  # "/Users/josiahbrown/Desktop/passwords.txt"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = "".join(password_list)  # Join the list to create a string
    password_entry.delete(0, END)
    password_entry.insert(0, password)  # Insert password string into GUI
    pyperclip.copy(password)  # Copy password to clipboard


# ---------------------------- SEARCH METHOD ------------------------------- #
def find_password():
    # Get the data in the website field
    website = web_entry.get().title()

    # Check to see if it exists in the current data.json file
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            pw = data[website]["password"]
            messagebox.showinfo(message=f"{website}", detail=f"Email: {email}\n"
                                                          f"Password: {pw}")
        else:
            messagebox.showerror(message=f"No details for {website} exist")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    web = web_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        web: {
            "email": email,
            "password": password,
        }
    }

    if len(web) == 0 or len(password) == 0:
        messagebox.showerror(title="Not Enough Info", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)  # Load data as a dictionary
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)  # Update dict with new data

            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)  # Dump data back into file
        finally:
            web_entry.delete(0, END)
            web_entry.focus()
            email_entry.delete(0, END)
            email_entry.insert(0, "josiahbrown321@gmail.com")
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# Labels
web_label = Label(text="Website:")
web_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
web_entry = Entry(width=21)
web_entry.grid(column=1, row=1, columnspan=1)
web_entry.focus()  # This puts the cursor inside this box upon launch
email_entry = Entry(width=35)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "josiahbrown321@gmail.com")  # Inserts my email by default
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Buttons
generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()