import turtle as t
import random

# Setup
window = t.Screen()
screen_x = 500
screen_y = 400
window.screensize(screen_x, screen_y)
window.bgcolor("black")
colors = ["red", "orange", "yellow", "green", "blue", "purple"]
turtles = []

# -- Functions --
# Ask for user bet
def ask_bet ():
    valid = False
    while not valid:
        bet = window.textinput(title="Scegli la tartaruga", prompt="Quale tartaruga vincerà?\nScegli un colore")
        if bet in colors:
            valid = True
    return bet

# Write the content at specified y cordinate at the center of the screen
def write_center(content, y):
    wt = t.Turtle()
    wt.hideturtle()
    wt.penup()
    wt.goto(0, y)
    wt.color("white")
    wt.write(content, align="center", font=("Arial", 20, "bold"))

# Setup and return an array of 6 turtles
def turtles_setup ():
    x_cord = (screen_y - 40) / 2 # Set the starting point to move the turtles (with margins)
    for color in colors:
        gas = t.Turtle()
        gas.shape("turtle")
        # Turtle initialization
        gas.penup()
        gas.color(color)
        gas.setpos(-230,x_cord)
        turtles.append(gas)
        x_cord -= 60
    return turtles

# Draw the finish line
def draw_finishline():
    fl = t.Turtle()
    fl.hideturtle()
    fl.penup()
    fl.color("white")
    rect_width = 10
    rect_height = 420
    fl.goto(230, rect_height / 2)
    fl.pendown()
    fl.begin_fill()
    fl.goto(230, -rect_height / 2)
    fl.goto(230 + rect_width, -rect_height / 2)
    fl.goto(230 + rect_width, rect_height / 2)
    fl.goto(230, rect_height / 2)
    fl.end_fill()

# Main
bet = ask_bet()
write_center(f'Welcome to the TURTLE RACE !! \nYour bet is: {bet}', 300)    
turtles = turtles_setup()
draw_finishline()

game = True
while game:
    for turtle in turtles:
        turtle.forward(random.randint(0, 20))
        if turtle.xcor() >= 230:
            game = False
            winning_color = turtle.pencolor()
            write_center(f'The winner is: {winning_color}!', 0)
if winning_color == bet:
    write_center("You Won" , -50)

window.exitonclick()
