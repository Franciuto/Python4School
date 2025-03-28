from game_data import *
import random
import time
import os
from prettytable import PrettyTable

print('Benvenuto nel gioco high or lower\n\nℹ Istruzioni ℹ\n ► Ti verranno presentate due opzioni\n ► Dovrai scegliere quella che reputi più seguita')

# Os CLI clear
if os.name == "nt":
    clear = "cls"
else:
    clear = "clear"

# Init game vars
game = False
ultimate_win = False

# Ask for start
start = input("Vuoi iniziare? (s/n): ").lower()
if start == "s":
    game = True
    os.system(clear)

# Function that returns a dictionary of a character from the list (avoid duplicates)
def random_account():
    already_solved = []
    # If all accounts have been guessed notify the user and quit
    if len(already_solved) == len(data):
        game = False
        ultimate_win = True
        pass
    r = random.randint(0, len(data))       
    while r in already_solved:
        r = random.randint(0, len(data))
    already_solved.append(r)
    return data[r]

# Function that returns a printable table for game UI
def make_table(account1, account2):
    table = PrettyTable()
    # Header definition
    table.field_names = ["", "Personaggio 1", "Personaggio 2"]

    # Rows definition
    table.add_row(["Nome", account1["name"], account2["name"]])
    table.add_row(["Paese", account1["country"], account2["country"]])
    table.add_row(["Descrizione", account1["description"], account2["description"]])

    # Left align
    table.align = "l"
    return table

# Function that checks if the user guess is correct by returning true
def check_correct(user_choice):
    pop1 = account1["follower_count"]
    pop2 = account2["follower_count"]

    if user_choice == "1":
        if pop1 > pop2:
            return True
        else:
            return False
    elif user_choice == "2":
        if pop2 > pop1:
            return True
        else:
            return False

round = 1
guess = 0
while game:
    os.system(clear)
    # Print the current random
    print(f'Round: {round}')

    # Choose 2 random accounts
    account1 = random_account()
    account2 = random_account()

    # Make and print the table with the content
    print(make_table(account1, account2))

    # Prompt the user for the most popular
    choice = input(f"Qual'è il più popolare? (1/2): ").lower()
    # Check for correct input
    while choice not in ["1" , "2"]:
        choice = input("Input non valido!\nQual'è il più popolare? (1/2): ")
        
    os.system(clear)
    # Check if the user choice is correct
    if check_correct(choice):
        print("Hai indovinato !!")
        guess += 1
    else:
        print("Non hai indovinato")
        game = False
    round += 1
    time.sleep(1)

if ultimate_win:
    print("Hai indovinato tutti gli account")

print(f"Hai indovinato {guess} account\nBye!!")