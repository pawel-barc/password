import re
import random
import hashlib
import json
import tkinter as tk
from tkinter import *

# Function to check if password meets security requirements
def check_password(password):
    if len(password) <= 8:
        return False
    elif not re.search("[a-z]", password):
        return False
    elif not re.search("[A-Z]", password):
        return False
    elif not re.search("[0-9]", password):
        return False
    elif not re.search("[!@#$%^&*]", password):
        return False
    else:
        return True
# Function to generate a password  
def generate_password():
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
    random.choice(characters)
    while True:
        password =''.join(random.choice(characters) for i in range(12))
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        if check_password(password):
            return password
        
# Function to encrypt password            
def encrypting(password):
        return hashlib.sha256(password.encode()).hexdigest()

# Function to display message in text widget
def display_msg(msg):
    text_disp.config(state=tk.NORMAL)
    text_disp.delete("1.0", tk.END)
    text_disp.insert(tk.END, msg)
    text_disp.config(state=tk.DISABLED)

# Function to verify password and display message
def verif_display():
    password = entry_password.get()
    if check_password(password):
        display_msg("Mot de passe valide")
    else:
        display_msg("Mot de passe non valide, Votre mot de passe doit comporter au moins 8 caractères et au moins un chiffre, une lettre et un caractère spécial")
        entry_password.delete(0, tk.END)

# Function to save password to file
def save_password():
    password = entry_password.get()
    if password:
        if check_password(password):
            pass_hash = encrypting(password)
            if file_save(pass_hash):
                passwds = "Mot de passe sauvegardé avec succès\n" + load_from_json_to_tkinter()
                display_msg(passwds)
            else:
                display_msg("Le mot de passe existe déjà dans la base de données")
        else:
            display_msg("Mot de passe non valide")
    else:
        display_msg("Veuillez saisir un mot de passe avant de sauvegarder")

# Function to save password to file
def file_save(password, filename="pass.json"):
    try:
        with open(filename, "r+") as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = []
    except FileNotFoundError:
        passwords = []
    if password not in passwords:
        passwords.append(password)
        with open(filename, "w+") as file:
            json.dump(passwords, file)
        return True
    else:
        return False
    
#Funtion to save password in text field    
def load_from_json_to_tkinter(filename="pass.json"):
    try:
        with open(filename, "r+") as file:
            try:
                passwords = json.load(file)
            except json.JSONDecodeError:
                passwords = []
    except FileNotFoundError:
        passwords = []
    string = ""
    for passwd in passwords:
        string += passwd + "\n"
    return string

# Function to toggle password visibility
def check():
    if show_pass.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")
    
# Main window
window = tk.Tk()
window.title("Vérificateur et Générateur de mot de passe")
window.config(bg="#31CECE")
window.geometry("720x400")

frame = Frame(window,width=60,height=80, bg='#A6E1EA')
# Widgets
label_password = tk.Label(frame,width=60,height=2,bg='#A6E1EA',font=("Helvetica", 15), text="Mot de passe :")
label_password.pack()

entry_password = tk.Entry(frame,width=30, borderwidth=4, font=("Helvetica", 12), show="*")
entry_password.pack(pady=2,)
password_entry = entry_password
password_entry.pack()

entry = tk.Entry
show_pass = tk.IntVar()
checkbutton = tk.Checkbutton(frame,width=20,font=("Helvetica", 12),bg='#A6E1EA', text='Afficher mot de passe', variable=show_pass, command=check)
checkbutton.pack()

button_verif = tk.Button(frame,width=22,font=("Arial", 12),text="Vérifier", bg="#31CECE", relief=RAISED, command=verif_display)
button_verif.pack()
button_generate = tk.Button(frame,width=22,font=("Arial", 12), text="Générer mot de passe", bg="#31CECE", relief=RAISED, command=generate_password)
button_generate.pack( pady=10)
button_save = tk.Button(frame,width=22,font=("Arial", 12), text="Sauvegarder", bg="#31CECE", relief=RAISED, command=save_password)
button_save.pack()

text_disp = tk.Text(frame,width=70, height=5,font=("Arial",12), state=tk.DISABLED)
text_disp.pack(pady=10)
frame.pack(expand=YES)
# Main loop launch
window.mainloop()