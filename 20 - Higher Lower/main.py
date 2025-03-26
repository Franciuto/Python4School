from game_data import *
import random
import tabulate

print('Benvenuto nel gioco high or lower\n\nℹ Istruzioni ℹ\n ► Ti verranno presentate due opzioni\n ► Dovrai scegliere quella che reputi più seguita')

def random_account():
    already_solved = []
    r = random.randint(0, len(data))       
    while r in already_solved:
        r = random.randint(0, len(data))
    already_solved.append(r)
    return data[r]

def make_table(account1, account2):
    
    pass
p1 = random_account()
p2 = random_account()
print(f'{p1}\n{p2}')