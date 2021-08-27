#!/Library/Frameworks/Python.framework/Versions/3.9/bin/python3.9

from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
# import pyperclip
import sqlite3 as sql

# ---------------------------- DATABASE INIT ------------------------------- #
# Connect to the DB file
conn = sql.connect('data.db')
cursor = conn.cursor()

# Create a new table if it does not exist
try:
    cursor.execute("SELECT * FROM info")
except sql.OperationalError:
    cursor.execute("CREATE TABLE info (website text, email text, password text)")
    conn.commit()
else:
    pass


def show_popup_window(title, message):
    """Create pop-up window using tkinter TopLevel"""
    popup = Toplevel(window)
    popup.title(title)
    popup.configure(padx=20, pady=20)

    # Add label to show message
    info_text = Label(popup, text=f"{message}\n")
    info_text.grid(column=0, row=0)

    # Add button to close window and destroy widget
    close_button = Button(popup, text="Close", command=popup.destroy)
    close_button.grid(column=0, row=1)

    # Show window
    popup.tkraise(window)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Returns a strong random password"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '*']

    # Get a random amount of characters of each type
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_numbers = [choice(numbers) for _ in range(randint(3, 7))]
    password_symbols = [choice(symbols) for _ in range(randint(6, 8))]

    # Concatenate the different types
    password_list = password_letters + password_numbers + password_symbols

    # Shuffle the password
    shuffle(password_list)

    # Join the list of characters, insert new password to GUI, and copy to clipboard
    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    # pyperclip.copy(password)


# ---------------------------- SEARCH METHOD ------------------------------- #
def find_password():
    """If the password exists, copies to clipboard"""
    # Get the data in the website field
    website = web_entry.get().title().lower()

    # Check to see if the site exists in the DB
    cursor.execute("SELECT * FROM info WHERE website=:site", {"site": website})
    curr_site = cursor.fetchone()

    # If info is found, copy the password and display a popup with all info
    try:
        curr_email = curr_site[1]
        curr_password = curr_site[2]
    except TypeError:
        show_popup_window("Error", "No information found.")
    else:
        # pyperclip.copy(curr_password)
        show_popup_window(f"{website}", f"Email: {curr_email}\n Password: {curr_password}\n\n"
                                        f"Password has been copied to your clipboard.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    """Saves the current field values as a new entry in the DB"""
    # Save the field values to variables and copy password
    web = web_entry.get().title().lower()
    email = email_entry.get()
    password = password_entry.get()
    # pyperclip.copy(password)

    # If no fields are empty
    if len(web) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showerror(title="Not Enough Info", message="Please don't leave any fields empty")
    else:
        # Select the site info if it already exists
        # If it exists, the password will not be added to the system as it would override the current value
        cursor.execute("SELECT * FROM info WHERE website=:site", {"site": web})
        curr_site = cursor.fetchone()
        if not curr_site:
            cursor.execute("INSERT INTO info VALUES (?, ?, ?)", (web, email, password))
            show_popup_window("Password Added!", f"The following info has been added to the system:\n\n"
                                                 f"website: {web}\n"
                                                 f"email: {email}\n"
                                                 f"password: {password}\n\n"
                                                 f"The password has been copied to your clipboard!")
            web_entry.delete(0, END)
            web_entry.focus()
            email_entry.delete(0, END)
            email_entry.insert(0, "josiahbrown321@gmail.com")
            password_entry.delete(0, END)
        else:
            show_popup_window("Error", "Looks like you have already entered information for that site.")


def close_window():
    """Closes the window after saving the data to the DB"""
    conn.commit()
    conn.close()
    window.destroy()


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
close_window_button = Button(text="CLOSE", width=10, height=5, highlightbackground='red', command=close_window)
close_window_button.grid(column=0, row=0)

window.mainloop()
