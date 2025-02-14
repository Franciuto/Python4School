valore = int(input("Inserisci valore: "))

while valore < 0:
    print("Inserire un valore positivo")
    valore = int(input("Inserisci valore: "))

n = 0

while n * n <= valore:
    if n * n == valore:
        print("Il numero è un quadrato perfetto")
        break
    n += 1
else:
    print("Il numero non è un quadrato perfetto")
