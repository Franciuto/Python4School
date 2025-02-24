string1 = input("Inserisci stringa 1: ")
string2 = input("Inserisci stringa 2: ")
resString = ""

if len(string1) > len(string2):
    lenght = len(string1)
else:
    lenght = len(string2)

for i in range (0 , lenght):
    if i < len(string1):
        resString += string1[i]
    if i < len(string2):
        resString += string2[i]

print(resString)