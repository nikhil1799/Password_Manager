from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import pandas
import json
import os

field_check = True

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

nr_letters = random.randint(8, 10)
nr_symbols = random.randint(2, 4)
nr_numbers = random.randint(2, 4)

password_list = []

password_letters = [random.choice(letters) for letter in range(nr_letters)]

password_symbols = [random.choice(symbols) for symbol in range(nr_symbols)]

password_numbers = [random.choice(numbers) for number in range(nr_numbers)]

pass_list = password_letters + password_numbers + password_symbols

random.shuffle(pass_list)

password = "".join(pass_list)


def pass_generator():
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)

    # ---------------------------- FIND PASSWORD ------------------------------- #


def website_check():

    website_search = website_input.get().capitalize()
    with open('data.json') as file:
        finder = json.load(file)

    for web_search in finder:

        if website_search == web_search:
            return False
        else:
            return True


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():

    website_check()
    website = website_input.get().capitalize()
    username = user_input.get()
    pas = password_input.get()

    if website_check() == False:
        messagebox.showinfo(title='Oops', message="Details for that site alreadys exist!")
        website = ''
        website_input.delete(0, END)

    if len(website) < 1 or len(username) < 1 or len(pas) < 1:
        messagebox.showinfo(title='Oops', message="Please don't leave any fields empty!")
    else:
        new_data = {
            website: {
                'Username/Email': username,
                'password': pas,
            }
        }
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)

        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)

            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)

        finally:
            website_input.delete(0, END)
            user_input.delete(0, END)
            password_input.delete(0, END)


def find_password():
    try:
        with open('data.json') as file:
            finder = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title='Error', message=f"No Data File Found")

    else:
        website_name = website_input.get().capitalize()

        for website in finder:

            if website == website_name:
                saved_user = finder[website]['Username/Email']
                saved_pass = finder[website]['password']

                messagebox.showinfo(title='Login Info',
                                    message=f"Username/Email: {saved_user} \nPassword: {saved_pass}")
            else:
                messagebox.showinfo(title='Error', message=f"No details for this website exist")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
password_image = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=password_image)
canvas.grid(column=1, row=0)

website_label = Label(text='Website: ')
website_label.grid(column=0, row=1)
user_label = Label(text='Email/Username: ')
user_label.grid(column=0, row=2)
password_label = Label(text='Password: ')
password_label.grid(column=0, row=3)

website_input = Entry(width=21)
website_input.focus()
website_input.grid(column=1, row=1)
user_input = Entry(width=38)
user_input.grid(column=1, row=2, columnspan=2)
password_input = Entry(width=21)
password_input.grid(column=1, row=3)

search_button = Button(text='Search', width=12, command=find_password)
search_button.grid(column=2, row=1)

generate_button = Button(text='Generate Password', command=pass_generator)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
