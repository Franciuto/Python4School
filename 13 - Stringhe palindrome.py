string = input("Inserisci stringa: ")
cleanString = ""
for lettera in string:
    if lettera.isalpha():
        cleanString += lettera

if cleanString == cleanString[::-1]:
    print("La stringa è palindroma")
else: 
    print("La stringa non è palindroma")