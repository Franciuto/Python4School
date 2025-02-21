# Declarations
charset = "abcdefghijklmnopqrstuvwxyz"
cypherText = ""

# Input
plaintext = input("Inserisci il messaggio in chiaro: ").lower()
toRot = int(input("Che rot vuoi effettuare? (1-13): "))
# Check for valid ROT
while toRot > 13 or toRot < 1:
    print("Inserisci un valore valido")
    toRot = int(input("Che rot vuoi effettuare? (1-13): "))

# Loop for every letter in the string "plaintext"
for letter in plaintext:
    if letter in charset: # If the letter is present in the charset  
        index = charset.index(letter)   # Search for the letter index
        result = index + toRot  # Add the desired rot to the number
        if result > charset.index("z"): # If the result of the rotation is above z
            result -= 26
        cypherText += charset[result] # Concatenate the result
    else: # If the letter isn't in the charset add it as it is
        cypherText += letter

print("Testo cifrato:", cypherText)
