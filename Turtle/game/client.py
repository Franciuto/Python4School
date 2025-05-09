import turtle
import socket
import threading
import json
import time

# Game settings
SCREEN_X = 500
SCREEN_Y = 400
WIN_X = SCREEN_X // 2 - 20

# Connection settings
SERVER_HOST = '192.168.180.32'  # Change this to the IP of the computer running the server
SERVER_PORT = 5678

class GameClient:
    def __init__(self):
        self.player_name = None
        self.client_socket = None
        self.my_id = None
        self.connected = False
        self.turtles = {}  # {player_id: turtle_obj}
        self.current_turn = None
        self.current_question = None
        self.game_started = False
        self.game_over = False
        self.window = None
        self.status_writer = None
        self.question_writer = None
        
        # Initialize UI
        self.setup_screen()
        self.init_writers()
        self.draw_finish_line()
        
    def setup_screen(self):
        """Set up the game window"""
        self.window = turtle.Screen()
        self.window.setup(width=SCREEN_X, height=SCREEN_Y)
        self.window.bgcolor("beige")
        self.window.title("Turtle Race with Quiz (Multiplayer)")
        self.window.tracer(0)  # Turn off animation
    
    def init_writers(self):
        """Initialize turtle writers for displaying text"""
        self.status_writer = turtle.Turtle()
        self.status_writer.hideturtle()
        self.status_writer.penup()
        self.status_writer.goto(0, SCREEN_Y // 2 - 40)
        
        self.question_writer = turtle.Turtle()
        self.question_writer.hideturtle()
        self.question_writer.penup()
        self.question_writer.goto(0, -SCREEN_Y // 2 + 40)
    
    def draw_finish_line(self):
        """Draw the finish line"""
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
        self.window.update()
    
    def create_turtle(self, player_id, color, position):
        """Create a turtle for a player"""
        if player_id in self.turtles:
            return
            
        turt = turtle.Turtle(shape="turtle")
        turt.color(color)
        turt.penup()
        turt.goto(position)
        self.turtles[player_id] = turt
        self.window.update()
    
    def connect_to_server(self):
        """Connect to the game server"""
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            self.connected = True
            
            # Send player name
            self.client_socket.send(json.dumps({"name": self.player_name}).encode('utf-8'))
            
            # Start thread to handle server messages
            receiver_thread = threading.Thread(target=self.receive_messages)
            receiver_thread.daemon = True
            receiver_thread.start()
            
            self.write_status("Connected to server. Waiting for game to start...")
        except Exception as e:
            self.write_status(f"Failed to connect: {e}")
    
    def receive_messages(self):
        """Receive and process messages from the server"""
        while self.connected:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if not data:
                    self.connected = False
                    self.write_status("Disconnected from server")
                    break
                
                # Handle multiple messages that might be received together
                try:
                    # Try to parse as a single message
                    message = json.loads(data)
                    self.process_message(message)
                except json.JSONDecodeError:
                    # Try to split multiple messages
                    parts = data.split('}{')
                    for i, part in enumerate(parts):
                        if i == 0:
                            if not part.startswith('{'):
                                part = '{' + part
                        elif i == len(parts) - 1:
                            if not part.endswith('}'):
                                part = part + '}'
                        else:
                            part = '{' + part + '}'
                        
                        try:
                            message = json.loads(part)
                            self.process_message(message)
                        except json.JSONDecodeError:
                            print(f"Failed to parse message: {part}")
                
            except Exception as e:
                print(f"Error receiving: {e}")
                self.connected = False
                break
    
    def process_message(self, message):
        """Process a message from the server"""
        msg_type = message.get('type')
        
        if msg_type == 'game_state':
            # Process initial game state
            players = message.get('players', {})
            for player_id, player_data in players.items():
                player_id = int(player_id)  # Convert from string to int
                self.create_turtle(
                    player_id, 
                    player_data['color'], 
                    player_data['position']
                )
            
            self.game_started = message.get('game_started', False)
            self.current_turn = message.get('current_turn')
            
            if self.game_started:
                self.write_status("Game in progress")
        
        elif msg_type == 'player_joined':
            # New player joined
            player_id = message.get('id')
            name = message.get('name')
            color = message.get('color')
            position = message.get('position')
            
            self.create_turtle(player_id, color, position)
            self.write_status(f"{name} joined the game")
            
        elif msg_type == 'player_left':
            # Player left the game
            player_id = message.get('id')
            if player_id in self.turtles:
                self.turtles[player_id].hideturtle()
                del self.turtles[player_id]
                self.write_status(f"A player left the game")
        
        elif msg_type == 'game_started':
            # Game has started
            self.game_started = True
            self.game_over = False
            self.write_status("Game started!")
        
        elif msg_type == 'next_turn':
            # Next player's turn
            self.current_turn = message.get('player_id')
            self.current_question = message.get('question')
            
            # Highlight current player
            for player_id, turt in self.turtles.items():
                if player_id == self.current_turn:
                    turt.shapesize(1.5)  # Make bigger
                else:
                    turt.shapesize(1.0)  # Normal size
            
            # Display question if it's my turn
            if self.current_turn == self.my_id:
                self.ask_question()
            else:
                self.write_question(f"Waiting for other player to answer...")
            
            self.window.update()
        
        elif msg_type == 'player_moved':
            # Player moved
            player_id = message.get('id')
            position = message.get('position')
            correct = message.get('correct')
            
            if player_id in self.turtles:
                turt = self.turtles[player_id]
                turt.goto(position)
                
                # Animate correct/wrong
                if correct:
                    original_color = turt.color()[0]
                    turt.color("gold")
                    self.window.update()
                    time.sleep(0.3)
                    turt.color(original_color)
                else:
                    original_color = turt.color()[0]
                    turt.color("gray")
                    self.window.update()
                    time.sleep(0.3)
                    turt.color(original_color)
                
                self.window.update()
        
        elif msg_type == 'game_over':
            # Game over, we have a winner
            winner = message.get('winner')
            winner_id = winner.get('id')
            winner_name = winner.get('name')
            winner_color = winner.get('color')
            
            self.game_over = True
            self.game_started = False
            
            # Highlight winner
            if winner_id in self.turtles:
                turt = self.turtles[winner_id]
                turt.shapesize(2.0)  # Make bigger
            
            self.write_status(f"{winner_name} wins the game!")
            self.write_question("Game Over! Click anywhere to exit.")
            self.window.update()
            self.window.exitonclick()
    
    def ask_question(self):
        """Ask the current math question"""
        if not self.current_question:
            return
            
        a = self.current_question.get('a')
        op = self.current_question.get('op')
        b = self.current_question.get('b')
        
        question_text = f"Your turn! What is {a} {op} {b}?"
        self.write_question(question_text)
        
        # Get answer
        answer = self.window.textinput("Quiz Time!", f"What is {a} {op} {b}?")
        
        # Send answer to server
        try:
            answer_int = int(answer) if answer is not None else None
            self.client_socket.send(json.dumps({
                "type": "answer",
                "answer": answer_int,
                "question": self.current_question
            }).encode('utf-8'))
        except ValueError:
            # Invalid input, send None
            self.client_socket.send(json.dumps({
                "type": "answer",
                "answer": None,
                "question": self.current_question
            }).encode('utf-8'))
    
    def write_status(self, message):
        """Write status message at the top of the screen"""
        self.status_writer.clear()
        self.status_writer.write(message, align="center", font=("Arial", 14, "bold"))
        self.window.update()
    
    def write_question(self, message):
        """Write question at the bottom of the screen"""
        self.question_writer.clear()
        self.question_writer.write(message, align="center", font=("Arial", 12, "normal"))
        self.window.update()
    
    def run(self):
        """Run the client"""
        self.write_status("Welcome to Turtle Race with Quiz!")
        self.write_question("Please enter your name to join")
        
        self.player_name = self.window.textinput("Player Name", "Enter your name:")
        if not self.player_name:
            self.player_name = "Guest"
        
        # Connect to server
        self.connect_to_server()
        
        # Main game loop
        while not self.game_over:
            self.window.update()
            time.sleep(0.05)  # Small delay to reduce CPU usage
        
        self.window.mainloop()

if __name__ == "__main__":
    client = GameClient()
    client.run()