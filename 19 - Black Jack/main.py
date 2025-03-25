import random

cards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]  # Ace is 1, face cards are 10
userHand = []
osHand = []

def dealInit():
    userHand.clear()
    osHand.clear()
    for i in range(2):
        userHand.append(random.choice(cards))
        osHand.append(random.choice(cards))

def isBlackjack(hand):
    return sum(hand) == 21

def isBust(hand):
    return sum(hand) > 21

def determineWinner():
    userTotal = sum(userHand)
    osTotal = sum(osHand)
    
    if isBust(userHand):
        return "Il computer vince (hai sballato)"
    elif isBust(osHand):
        return "Il player ha vinto (il computer ha sballato)"
    elif userTotal > osTotal:
        return "Il player ha vinto"
    elif osTotal > userTotal:
        return "Il computer vince"
    else:
        return "Pareggio"

# Main game loop
def playGame():
    dealInit()
    
    # Show initial hands
    print(f"La tua mano: {userHand}, totale: {sum(userHand)}")
    print(f"Prima carta del computer: {osHand[0]}")
    
    # Player's turn
    playerDone = False
    while not playerDone:
        if sum(userHand) >= 21:
            playerDone = True
            continue
            
        choice = input("Vuoi un'altra carta? (s/n): ").lower()
        if choice == 's':
            userHand.append(random.choice(cards))
            print(f"La tua mano: {userHand}, totale: {sum(userHand)}")
        else:
            playerDone = True
    
    # Computer's turn
    while sum(osHand) < 17:  # Computer hits until it reaches 17 or higher
        osHand.append(random.choice(cards))
    
    # Show final hands
    print(f"La tua mano finale: {userHand}, totale: {sum(userHand)}")
    print(f"Mano finale del computer: {osHand}, totale: {sum(osHand)}")
    
    # Determine winner
    print(determineWinner())

# Start the game
playGame()