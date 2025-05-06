import turtle as t
import random

# -- FUNCTIONS --
# Function to get a random color
def get_randColor ():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to draw a circle
def draw_circle (radius):
    gas.color(get_randColor())
    gas.begin_fill()
    gas.circle(radius)
    gas.end_fill()

# Function to draw a line of circle
def draw_line ():
    for i in range(10):
        draw_circle(radius)
        gas.forward(60)

# Radius of the circles made
radius = 10
# Window setup
window = t.Screen()
window.bgcolor("white")
# Set color mode to RGB
t.colormode(255)

gas = t.Turtle()
gas.speed(0)
gas.hideturtle()    # To hide the turtle
gas.penup()     # To hide the turtle line

y = 300     # Starting Y
x = -255    # X position (costant)

# Make a square of points 10x10
for i in range(10):
    gas.setpos(-255, y)     # Set position for turtle
    draw_line()       # Draw a line of circles
    y -= 60         # Go below to write the next line

window.onclick()