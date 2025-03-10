import os
import random

# ASCII ART
vite5 = """
 _________
 |/      |
 |      (_)
 |      \\|/
 |       |
 |      / \\
 |
_|___
"""
vite4 = """
 _________
 |/      |
 |      (_)
 |      \\|/
 |       |
 |      
 |
_|___
"""
vite3 = """
 _________
 |/      |
 |      (_)
 |      \\|/
 |       
 |      
 |
_|___
"""
vite2 = """
 _________
 |/      |
 |      (_)
 |      
 |       
 |      
 |
_|___
"""
vite1 = """ 
 _________
 |/      |
 |      
 |      
 |       
 |      
 |
_|___
"""

# CLEAR SCREEN
def clear ():
# For Windows
    if os.name == 'nt':
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

# DRAW ASCII-ART RELATED TO USER LIFES
def draw (life):
    match life:
        case 5:
            print(vite1)
        case 4:
            print(vite2)
        case 3:
            print(vite3)
        case 2:
            print(vite4)
        case 1:
            print(vite5)

# PRINT THE WORD
def print_word (word_len):
    out = " ".join(game)
    print(out)

# OPEN THE WORDLIST FILE 
wordlist = "wordlist.txt"
file = open(wordlist , "r")
words = file.read().splitlines()
words = list(words)     # Combine the words in a list

# ------- GAME START -------

# PICK A RANODM WORD FROM THE SOURCE FILE
word = list(random.choice(words))
word_len = len(word)       # Save the word lenght

# DECLARATION
vite = 5
global game     # Variable to store the guessing progress

# INITIALIZE GAME VECTOR
game = []
# Initialize the vector with "_"
for i in range (0 , word_len):
    game.append("_")

# GREETINGS
print(f"Benvenuto nel gioco dell'impiccato!!")

# ROUND INIT
# Continue playing until all letters have been guessed or no lifes left
while "_" in game and vite > 0:
        draw(vite)      # Print the ASCII art   
        print_word(word_len)    # Print the word

        gameIn = input("\nInserisci una lettera o indovina la parola: ").lower()
        if len(gameIn) > 1:     # If the input is not a single letter but a string check if it's the match for the entire word
            if gameIn == "".join(word):
                break
            else:
                vite = 0
                break
        elif gameIn in word:    # If the input is a single letter check if it's in the word and move every letters in the game
            for i in range (0 , word_len):
                if word[i] == gameIn:
                    game[i] = gameIn
        else:
            vite -= 1
        clear()

clear()
if vite != 0:
    print(f'Congratulazioni hai vinto con {vite} vite')
else:
    print(f'Hai perso!\n\nLa parola era "{"".join(word)}"')