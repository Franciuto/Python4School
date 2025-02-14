import re
raw = input("Inserisci operazione: ")
numbers = re.split(r'[^0-9]', raw)

def calcOperation(n1 , n2, op):
    if op == "+":
        return n1 + n2
    elif op == "-":
        return n1 - n2
    elif op == "*":
        return n1 * n2
    elif op == "/":
        return n1 / n2
    return("Operazione non supportata")

n1 = raw[0]
op = raw[1]
n2 = raw[2]

print("=" , calcOperation(int(n1) ,  int(n2), op))
