string = input("Inserisci stringa: ")
string = string.replace(" ","")

if string == string[::-1]:
    print("La stringa è palindroma")
else: 
    print("La stringa non è palindroma")