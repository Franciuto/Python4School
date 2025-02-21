# Similar to "15 - Simple ROT.py" but takes care of the Uppercase letters
charset = "abcdefghijklmnopqrstuvwxyz"
cypherString = ""

# Input
plaintext = input("Inserisci il messaggio in chiaro: ")
toRot = int(input("Che rot vuoi effettuare? (1-13): "))
# Check for valid ROT
while toRot > 13 or toRot < 1:
    print("Inserisci un valore valido")
    toRot = int(input("Che rot vuoi effettuare? (1-13): "))

def rot (letter, toRot):
    letter = letter.lower()
    index = charset.index(letter)   # Search for the letter index
    result = index + toRot  # Add the desired rot to the number
    if result > charset.index("z"): # If the result of the rotation is above z
        result -= 26
    return charset[result] # Return the rotated letter


for letter in plaintext:
    if letter.lower() in charset:
        if letter.islower():
            cypherString += rot(letter, toRot).lower()
        elif letter.isupper():
            cypherString += rot(letter, toRot).upper()
    else:
        cypherString += letter

print(f'La stringa cifrata con rot{toRot} è: {cypherString}')