import random

numeri = list()
somma = 0

# Generazione lista con numeri
for i in range (1, 20):
    numero = random.randint(1, 100)
    numeri.append(numero)
    somma += numero

# Calcolo media e stampa
print("Lista di numeri casuali")
print(numeri)
media = somma / len(numeri)
print(f'La media è {media}')