name1 = input("Inserisci nome 1: ").lower()
name2 = input("Inserisci nome 2: ").lower()

print(f'{name1} {name2}')
string = "true love"

def calculate_love_score(name1, name2):
    p1, p2 = 0, 0
    for letter in name1:
        if letter in string:
            p1 += 1
    for letter in name2:
        if letter in string:
            p2 += 1
    return str(p1) + str(p2)

print(calculate_love_score(name1, name2))