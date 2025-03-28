import json
import os
import time
from machine import *

# System clear
if os.name == "nt":
    clear = "cls"
else:
    clear = "clear"

def load_database():
    try:
        with open("users_db.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # Se il file non esiste, crea un database di default
        default_db = [
            {
                "username": "admin",
                "password": "admin",
                "balance": 10000000
            }
        ]
        save_database(default_db)
        return default_db

def save_database(db):
    with open("users_db.json", "w") as file:
        json.dump(db, file, indent=4)

def update_database(balance,username , db):
    for user in db:
        if user['username'] == username:
            user['balance'] = balance
            save_database(db)

def auth():
    while True:
        username_req = input("Username: ").strip()
        password_req = input("Password: ").strip()
        
        if not username_req or not password_req:
            print("Username and password cannot be empty!!")
            continue
        
        return (username_req, password_req)

def login(login_datas, db):
    username, password = login_datas
    
    for user in db:
        if user['username'] == username and user['password'] == password:
            print("Login successful!")
            return user  # Restituisce l'utente trovato
    
    print("Invalid username or password.")
    time.sleep(1)
    os.system(clear)
    return None

def register(login_datas, db):
    username, password = login_datas
    
    if not uniq_username(username, db):
        print("Username already used")
        return None
    
    new_user = {
        "username": username,
        "password": password,
        "balance": 0
    }
    db.append(new_user)
    save_database(db)
    print("Registration successful!")
    return new_user

def uniq_username(username, db):
    return all(user['username'] != username for user in db)

def show_userdata(username, balance):
    print("\n=== DETTAGLI UTENTE ===")
    print(f"Username: {username}")
    print(f"Saldo: {balance}")
    print("======================")

def menu ():
    print(" -- MENU --")
    chose = input("Buy:\n1. Cappuccino\n2. Espresso\n3. Latte\n\nManage:\n4. Off\n5. Logout\n")
    match chose:
        case "1":
            make(MENU["cappuccino"])
        case "2":
            pass
        case "3":
            pass
        case "4":
            pass
        case "5":
            pass

def make(beverage):
    cost = beverage["cost"]
    if balance < cost:
        print("Not enough money")
        time.sleep(1)
        os.system[clear]
        menu()
    for ingredient in beverage["ingredients"]:
        if ingredient == "water":
            needed = beverage["ingredients"]["water"]
            if needed > acqua:
                print("Non abbastanza acqua")
                menu()
    
    
    
def main():
    # Carica il database all'avvio
    database = load_database()
    current_user = None

    print("Benvenuto nella macchina del caffè!")

    while not current_user:
        choice = input("\nAUTENTICAZIONE:\n1. Login\n2. Register\n(1/2): ").strip()
        
        if choice == "1":
            login_data = auth()
            current_user = login(login_data, database)
        
        elif choice == "2":
            register_data = auth()
            current_user = register(register_data, database)
            if current_user:
                time.sleep(1)
                os.system(clear)
        
        else:
            print("Scelta non valida. Inserire 1 o 2")

    os.system(clear)
    print(f"\nBenvenuto, {current_user['username']}!")

    global username
    global balance
    username = current_user["username"]
    balance = current_user["balance"]

    global latte, acqua, caffè
    latte = resources["latte"]
    acqua = resources["acqua"]
    caffè = resources["caffè"]

    show_userdata(username, balance)
    menu()
    update_database(balance, username, database)
    

main()