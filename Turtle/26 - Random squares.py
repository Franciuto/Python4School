import turtle
import random

finestra = turtle.Screen()
finestra.bgcolor("white")

t = turtle.Turtle()
t.speed(1)  
t.hideturtle()

# Funzione per generare un colore casuale
def colore_casuale():
    r = random.random()
    g = random.random()
    b = random.random()
    return (r, g, b)

# Funzione per disegnare un quadrato 
def disegna_quadrato(lato):
    t.fillcolor(colore_casuale())
    t.begin_fill()
    
    for _ in range(4):
        t.forward(lato)
        t.left(90)
    
    t.end_fill()

numero_quadrati = int(input("Quanti quadrati vuoi disegnare? "))

lato_quadrato = 50

for _ in range(numero_quadrati):
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    
    t.penup()
    t.goto(x, y)
    t.pendown()
    
    disegna_quadrato(lato_quadrato)

finestra.exitonclick()