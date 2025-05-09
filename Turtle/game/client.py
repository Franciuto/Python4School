import socket
import json
import threading
import turtle
import game_logic
import time
import queue

class GameClient:
    def __init__(self):
        self.socket = None
        self.player_num = None
        self.player_color = None
        self.player_name = "Player"
        self.game_state = {
            "red_pos": (-game_logic.SCREEN_X // 2 + 20, 50),
            "blue_pos": (-game_logic.SCREEN_X // 2 + 20, -50),
            "turn": 0,
            "winner": None,
            "current_question": None,
            "game_started": False,
            "player_ready": [False, False]
        }
        self.client_names = ["Player 1", "Player 2"]
        self.window = None
        self.red_turtle = None
        self.blue_turtle = None
        self.connected = False
        self.lock = threading.Lock()
        # Use a queue to pass messages from network thread to main thread
        self.message_queue = queue.Queue()
        # Flag to ask for input in main thread
        self.need_input = False
        self.current_question = None
        
    def connect_to_server(self, host, port=8000):
        """Connect to the game server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            # Start a thread to receive messages from the server
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def receive_messages(self):
        """Receive and process messages from the server."""
        try:
            while self.connected and self.socket:
                try:
                    data = self.socket.recv(1024)
                    if not data:
                        break
                    
                    message = json.loads(data.decode())
                    
                    # Put message in queue for main thread to process
                    self.message_queue.put(message)
                except json.JSONDecodeError:
                    print("Received invalid JSON data")
                except Exception as e:
                    print(f"Error in receive loop: {e}")
                    break
                
        except Exception as e:
            print(f"Error receiving message: {e}")
        finally:
            self.connected = False
            print("Disconnected from server")
    
    def process_messages(self):
        """Process messages in the main thread."""
        while not self.message_queue.empty():
            message = self.message_queue.get()
            message_type = message.get("type")
            
            if message_type == "player_info":
                self.player_num = message.get("player_num")
                self.player_color = message.get("color")
                print(f"You are player {self.player_num + 1} ({self.player_color})")
            
            elif message_type == "game_state":
                with self.lock:
                    self.game_state = message.get("state")
                    self.client_names = message.get("client_names", self.client_names)
                    
                    # Check if it's my turn
                    is_my_turn = (self.game_state["turn"] % 2 == self.player_num)
                    has_question = self.game_state["current_question"] is not None
                    is_game_active = self.game_state["game_started"] and not self.game_state["winner"]
                    
                    if is_my_turn and has_question and is_game_active:
                        self.need_input = True
                        self.current_question = self.game_state["current_question"]
                
                self.update_display()
    
    def send_message(self, message):
        """Send a message to the server."""
        if not self.connected:
            return False
        
        try:
            self.socket.send(json.dumps(message).encode())
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
            return False
    
    def mark_ready(self, name):
        """Mark this player as ready to start the game."""
        self.player_name = name
        return self.send_message({
            "type": "ready",
            "name": name
        })
    
    def submit_answer(self, answer):
        """Submit an answer to the current question."""
        return self.send_message({
            "type": "answer",
            "answer": answer
        })
    
    def initialize_game(self):
        """Set up the game UI."""
        self.window = game_logic.setup_screen(f"Turtle Race with Quiz - {self.player_name}")
        self.red_turtle, self.blue_turtle = game_logic.init_turtles()
        game_logic.draw_finish_line()
        
        # Update positions if game already started
        with self.lock:
            if self.game_state["game_started"]:
                self.red_turtle.goto(*self.game_state["red_pos"])
                self.blue_turtle.goto(*self.game_state["blue_pos"])
    
    def update_display(self):
        """Update the game display based on current state."""
        if not self.window or not self.red_turtle or not self.blue_turtle:
            return
        
        with self.lock:
            # Update turtle positions
            if "red_pos" in self.game_state and "blue_pos" in self.game_state:
                self.red_turtle.goto(*self.game_state["red_pos"])
                self.blue_turtle.goto(*self.game_state["blue_pos"])
            
            # If there's a winner, announce it
            if self.game_state.get("winner"):
                winner_color = self.game_state["winner"]
                winner_index = 0 if winner_color == "red" else 1
                winner_name = self.client_names[winner_index] if winner_index < len(self.client_names) else "Unknown"
                game_logic.announce_winner(f"{winner_color} ({winner_name})")
    
    def run(self):
        """Run the game client."""
        # Get server details
        host = turtle.textinput("Connect to Game", "Enter server IP address:")
        if not host:
            return
        
        # Initialize game display with wait message before connecting
        self.window = game_logic.setup_screen("Turtle Race with Quiz - Connecting...")
        game_logic.write_center("Connecting to server...", y=0)
        
        # Force a single update before trying to connect
        try:
            self.window.update()
        except:
            return
        
        # Connect to server
        if not self.connect_to_server(host):
            try:
                self.window.clear()
                game_logic.write_center("Failed to connect to server.", y=0)
                self.window.update()
                time.sleep(3)
            except:
                pass
            return
        
        # Update connection status
        self.window.clear()
        game_logic.write_center("Connected to server...", y=50)
        game_logic.write_center("Waiting for player information.", y=0)
        
        # Wait for player info from server
        connecting_time = 0
        while self.player_num is None and self.connected and connecting_time < 20:  # 20 second timeout
            try:
                self.window.update()
                self.process_messages()  # Process any pending messages
            except:
                break
            connecting_time += 0.1
            time.sleep(0.1)
        
        if not self.connected or self.player_num is None:
            try:
                self.window.clear()
                game_logic.write_center("Connection failed or timed out!", y=0)
                self.window.update()
                time.sleep(3)
            except:
                pass
            return
            
        # Get player name - make sure we have player_num set
        player_str = str(self.player_num + 1) if self.player_num is not None else "?"
        color_str = self.player_color if self.player_color else "unknown"
        
        name = turtle.textinput("Player Name", f"You are Player {player_str} ({color_str}). Enter your name:")
        if not name:
            name = f"Player {player_str}"
        
        # Initialize game proper
        self.player_name = name
        self.initialize_game()
        
        # Mark ready to play
        self.mark_ready(name)
        game_logic.write_center(f"Welcome {name}! Waiting for other player...", y=0)
        
        # Main game loop
        try:
            while self.connected:
                try:
                    if self.window:
                        self.window.update()
                except:
                    break
                
                # Process any pending messages first
                self.process_messages()
                
                # Handle input for questions
                if self.need_input and self.current_question:
                    # Ask the question
                    q = self.current_question
                    a, op, b = q["a"], q["op"], q["b"]
                    prompt = f"What's {a} {op} {b}?"
                    
                    try:
                        answer = turtle.textinput(f"Your Turn ({self.player_color})", prompt)
                        self.submit_answer(answer)
                        self.need_input = False  # Reset input request
                    except:
                        break
                
                time.sleep(0.1)  # Small delay to avoid high CPU usage
                
        except turtle.Terminator:
            pass  # Window was closed
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            # Close connection
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass

if __name__ == "__main__":
    client = GameClient()
    try:
        client.run()
    except KeyboardInterrupt:
        print("Client stopped by user")
