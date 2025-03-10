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
            print(vite5)
        case 4:
            print(vite4)
        case 3:
            print(vite3)
        case 2:
            print(vite2)
        case 1:
            print(vite1)

# DRAW PLACEHOLDERS
def print_word (word_lenght):
    out = " ".join(game)
    print(out)

# OPEN WORDLIST
wordlist = "wordlist.txt"
file = open(wordlist , "r")
words = file.read().splitlines()
words = list(words)

# ------ PROGRAM START -------
# Greetings
print(f"Benvenuto nel gioco dell'impiccato!!")

# PICK A RANODM WORD FROM THE SOURCE
word = random.choice(words)
word_len = len(word)

# INITIALIZE GAME VECTOR
global game
game = []
for i in range (0 , word_len):
    game.append("_")

draw(5)
print_word(word_len)

