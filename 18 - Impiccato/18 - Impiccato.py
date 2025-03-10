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

# DRAW ASCII-ART
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

# DRAW PLACEHOLDERS
def print_word (word_len):
    out = " ".join(game)
    print(out)

# OPEN WORDLIST
wordlist = "wordlist.txt"
file = open(wordlist , "r")
words = file.read().splitlines()
words = list(words)

# ------ PROGRAM START -------

# PICK A RANODM WORD FROM THE SOURCE
word = list(random.choice(words))
word_len = len(word)

# DECLARATION
vite = 5
global game

# INITIALIZE GAME VECTOR
game = []
for i in range (0 , word_len):
    game.append("_")

# GREETINGS
print(f"Benvenuto nel gioco dell'impiccato!!")

# ROUND INIT
while "_" in game and vite > 0:
        draw(vite)
        print_word(word_len)

        gameIn = input("\nInserisci una lettera o indovina la parola: ").lower()
        if len(gameIn) > 1:
            if gameIn == "".join(word):
                break
            else:
                vite = 0
                break
        elif gameIn in word:
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