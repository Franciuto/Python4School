import turtle

# Imposta lo schermo
screen = turtle.Screen()
screen.bgcolor("light blue")

# Imopstazione Turtle
t = turtle.Turtle()
t.speed(3)
t.hideturtle()

def draw_rectangle(width, height, color):
    t.pendown()
    t.color("black", color)
    t.begin_fill()
    for i in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.penup()

def draw_triangle(size, color):
    t.pendown()
    t.color("black", color)
    t.begin_fill()
    for _ in range(3):
        t.forward(size)
        t.left(120)
    t.end_fill()
    t.penup()

t.penup()
t.goto(-50, -50)

# Casa principale
draw_rectangle(100, 80, "yellow")

# Tetto
t.goto(-50, 30)  
draw_triangle(100, "red")

# Porta
t.goto(-30, -50)  
draw_rectangle(25, 40, "brown")

# Finestra
t.goto(10, -20) 
draw_rectangle(20, 20, "light blue")

screen.mainloop()
