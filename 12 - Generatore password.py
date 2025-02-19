#Password Generator Project
import random
letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = list("0123456789")
symbols = list("!#$%&()*+,-./:;<=>?@[]^_{|}~")

def livelloFacile(nr_letters, nr_symbols, nr_numbers):
    passwordFacile = []
    # Aggiungo nr_letters random nella password
    for i in range (0 , nr_letters):
        rand = random.randint(0, len(letters))
        passwordFacile.append(letters[rand])

    # Aggiungo nr_symbol random nella password
    for i in range (0 , nr_symbols):
        rand = random.randint(0, len(symbols))
        passwordFacile.append(symbols[rand])

    # Aggiungo nr_numbers random nella password
    for i in range (0 , nr_numbers):
        rand = random.randint(0, len(numbers))
        passwordFacile.append(numbers[rand])
    
    return passwordFacile

def livelloMedio(password):
    random.shuffle(password)
    passwordFinale = "".join(password)
    return passwordFinale

print("Benvenuto nel generatore di password!")
nr_letters= int(input("Quante lettere vuoi nella tua password? ")) 
nr_symbols = int(input("Quanti simboli vuoi? "))
nr_numbers = int(input("Quanti numeri vuoi? "))

print(livelloMedio(livelloFacile(nr_letters, nr_symbols, nr_numbers)))
