from turtle import *

window = Screen()

gas = Turtle()
gas.speed(0)

l = 1

for i in range (200):
    gas.forward(l)
    gas.left(20)
    l += 1

window.exitonclick()