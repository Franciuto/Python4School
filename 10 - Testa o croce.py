import random

choose = int(input("Testa (0) o Croce (1): "))

lancio = random.randint(0, 1)
continueGame = 1

while continueGame != 0:
    if lancio == 0:
        print("È uscito Testa")
    else:
        print("È uscito Croce")

    if choose == lancio:
        print("Hai vinto!!")
    else:
        print("Hai perso")

    continueGame = input("Vuoi continuare a giocare (s/n): ")
    if continueGame == "n":
        continueGame = 0
        print("Goodbye")
