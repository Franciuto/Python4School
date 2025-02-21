#Password Generator Project
import random
letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = list("0123456789")
symbols = list("!#$%&()*+,-./:;<=>?@[]^_{|}~")

def livelloFacile(nr_letters, nr_symbols, nr_numbers):
    passwordFacile = []
    # Aggiungo nr_letters random nella password
    for i in range (0 , nr_letters):
        passwordFacile.append(random.choice(letters))

    # Aggiungo nr_symbol random nella password
    for i in range (0 , nr_symbols):
        passwordFacile.append(random.choice(symbols))

    # Aggiungo nr_numbers r22andom nella password
    for i in range (0 , nr_numbers):
        passwordFacile.append(random.choice(numbers))
    
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
