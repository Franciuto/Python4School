import turtle
import random

# Screen dimensions
screen_x = 500
screen_y = 400
win_x = screen_x // 2 - 20  # 20 pixels margin

# Window setup
def setup_screen():
    window = turtle.Screen()
    window.setup(width=screen_x, height=screen_y)
    window.bgcolor("beige")
    window.title("Turtle Race with Quiz (offline)")
    return window

# Create turtles
def init_turtles():
    red_turtle = turtle.Turtle(shape="turtle")
    red_turtle.color("red")
    red_turtle.penup()
    red_turtle.goto(-screen_x // 2 + 20, 50)

    blue_turtle = turtle.Turtle(shape="turtle")
    blue_turtle.color("blue")
    blue_turtle.penup()
    blue_turtle.goto(-screen_x // 2 + 20, -50)

    return red_turtle, blue_turtle

# Draw finish line
def draw_finish_line():
    line = turtle.Turtle()
    line.hideturtle()
    line.penup()
    line.color("black")
    line.goto(win_x, -screen_y // 2)
    line.setheading(90)
    line.pensize(3)
    # Linea tratteggiata
    for _ in range(20):
        line.pendown()
        line.forward(screen_y / 20)
        line.penup()
        line.forward(screen_y / 20)

# Random op generator
def generate_question():
    op = random.choice(['+', '-', '*', '/'])
    if op == '/':
        # integer division facilitator
        b = random.randint(1, 10)
        a = b * random.randint(0, 10)
    else:
        a = random.randint(0, 30)
        b = random.randint(0, 30)
    return a, op, b

# Ask and if correct move
def ask_and_move(turt):
    a, op, b = generate_question()
    prompt = f"What's {a} {op} {b}?"
    
    answer = turtle.textinput(f'Round {turn}', prompt)
    if answer is None:
        return False  # cancel = wrong
    try:
        ans = int(answer)
    except ValueError:
        return False  # if not ingere is not valid

    # Find correct
    if op == '+':
        correct = a + b
    elif op == '-':
        correct = a - b
    elif op == '*':
        correct = a * b
    else:
        correct = a // b

    # Move if correct
    if ans == correct:
        turt.forward(20)
        return True
    return False

# Write at y position center line
def write_center(msg, y=0):
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("black")
    writer.goto(0, y)
    writer.write(msg, align="center", font=("Arial", 20, "bold"))

def race():
    window = setup_screen()
    draw_finish_line()  # draw the finish line
    turtles = init_turtles()
    global turn
    turn = 0
    winner = None

    while not winner:
        current = turtles[turn % len(turtles)]
        ask_and_move(current)
        
        # Check for win
        if current.xcor() >= win_x:
            winner = current
            break
        turn += 1

    # Announce winner
    winner_color = winner.color()[0].capitalize()
    write_center(f"{winner_color} turtle wins!", y=0)
    window.exitonclick()

race()
