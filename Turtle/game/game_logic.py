import random
import turtle

# Screen dimensions
SCREEN_X = 500
SCREEN_Y = 400
WIN_X = SCREEN_X // 2 - 20  # 20 pixels margin

def setup_screen(title):
    """Setup the turtle screen with specified dimensions and title."""
    window = turtle.Screen()
    window.setup(width=SCREEN_X, height=SCREEN_Y)
    window.bgcolor("beige")
    window.title(title)
    return window

def init_turtles():
    """Initialize the red and blue turtles."""
    red_turtle = turtle.Turtle(shape="turtle")
    red_turtle.color("red")
    red_turtle.penup()
    red_turtle.goto(-SCREEN_X // 2 + 20, 50)

    blue_turtle = turtle.Turtle(shape="turtle")
    blue_turtle.color("blue")
    blue_turtle.penup()
    blue_turtle.goto(-SCREEN_X // 2 + 20, -50)

    return red_turtle, blue_turtle

def draw_finish_line():
    """Draw a dashed finish line."""
    line = turtle.Turtle()
    line.hideturtle()
    line.penup()
    line.color("black")
    line.goto(WIN_X, -SCREEN_Y // 2)
    line.setheading(90)
    line.pensize(3)
    # Dashed line
    for _ in range(20):
        line.pendown()
        line.forward(SCREEN_Y / 20)
        line.penup()
        line.forward(SCREEN_Y / 20)

def generate_question():
    """Generate a random math question."""
    op = random.choice(['+', '-', '*', '/'])
    if op == '/':
        # Integer division facilitator
        b = random.randint(1, 10)
        a = b * random.randint(0, 10)
    else:
        a = random.randint(0, 30)
        b = random.randint(0, 30)
    return a, op, b

def check_answer(a, op, b, answer):
    """Check if the given answer is correct."""
    if answer is None:
        return False  # Cancel = wrong
    
    try:
        ans = int(answer)
    except ValueError:
        return False  # If not integer, not valid
    
    # Calculate correct answer
    if op == '+':
        correct = a + b
    elif op == '-':
        correct = a - b
    elif op == '*':
        correct = a * b
    else:
        correct = a // b
    
    return ans == correct

def write_center(msg, y=0):
    """Write a message centered at y position."""
    writer = turtle.Turtle()
    writer.hideturtle()
    writer.penup()
    writer.color("black")
    writer.goto(0, y)
    writer.write(msg, align="center", font=("Arial", 20, "bold"))

def move_turtle(turtle_instance, distance=20):
    """Move the turtle forward by the specified distance."""
    turtle_instance.forward(distance)

def is_winner(turtle_instance):
    """Check if the turtle has reached the finish line."""
    return turtle_instance.xcor() >= WIN_X

def announce_winner(color):
    """Display the winner announcement."""
    write_center(f"{color.capitalize()} turtle wins!", y=0)

def clear_announcements():
    """Clear any announcements on the screen."""
    # We need to clear the entire screen and redraw everything except announcements
    turtle.clear()  # This clears only the "unnamed" turtle's drawings
