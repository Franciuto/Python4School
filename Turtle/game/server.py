import socket
import threading
import json
import random
import time
import game_logic
import turtle
import queue

class GameServer:
    def __init__(self, host='0.0.0.0', port=8000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.clients = []
        self.client_addresses = []
        self.client_names = ["", ""]
        self.game_state = {
            "red_pos": (-game_logic.SCREEN_X // 2 + 20, 50),
            "blue_pos": (-game_logic.SCREEN_X // 2 + 20, -50),
            "turn": 0,
            "winner": None,
            "current_question": None,
            "game_started": False,
            "player_ready": [False, False]
        }
        self.lock = threading.Lock()  # For thread-safe operations on game state
        self.window = None
        self.red_turtle = None
        self.blue_turtle = None
        self.accept_thread = None
        # Queue for turtle operations from threads
        self.ui_queue = queue.Queue()
        # Set server socket to non-blocking
        self.running = True
        self.connection_ready = False
        
    def start_server(self):
        """Start the game server and listen for client connections."""
        try:
            # Create server socket
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(2)  # Maximum 2 players
            # Set socket to non-blocking
            self.server_socket.setblocking(False)
            
            print(f"Server started on {self.host}:{self.port}")
            print("Waiting for players to connect...")
            
            # Setup turtle screen first
            self.window = game_logic.setup_screen("Turtle Race with Quiz (Server) - Waiting for players...")
            game_logic.write_center("Waiting for 2 players to connect...", y=0)
            
            # Main server loop - everything happens here now
            self.main_loop()
            
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            if self.server_socket:
                self.server_socket.close()
    
    def main_loop(self):
        """Main loop that handles both UI updates and client connections."""
        game_started = False
        
        try:
            # Main loop
            while self.running:
                # Update UI
                if self.window:
                    self.window.update()
                
                # Check for new connections if not full
                if len(self.clients) < 2:
                    try:
                        client_socket, client_address = self.server_socket.accept()
                        
                        # Assign player number (0 or 1)
                        player_num = len(self.clients)
                        player_color = "red" if player_num == 0 else "blue"
                        
                        # Send player info to the client
                        client_socket.send(json.dumps({
                            "type": "player_info",
                            "player_num": player_num,
                            "color": player_color
                        }).encode())
                        
                        # Add client to our lists
                        self.clients.append(client_socket)
                        self.client_addresses.append(client_address)
                        
                        print(f"Player {player_num + 1} ({player_color}) connected from {client_address}")
                        
                        # Update waiting message
                        if len(self.clients) == 1 and self.window:
                            self.window.clear()
                            game_logic.write_center("1 player connected. Waiting for 1 more...", y=0)
                        
                        # Make socket non-blocking
                        client_socket.setblocking(False)
                        
                        # Start a thread to handle client messages
                        client_thread = threading.Thread(target=self.handle_client, args=(client_socket, player_num))
                        client_thread.daemon = True
                        client_thread.start()
                        
                        # Check if both players are connected
                        if len(self.clients) == 2:
                            print("Both players connected. Game can start.")
                            if self.window:
                                self.window.clear()
                                game_logic.write_center("Both players connected! Waiting for players to be ready...", y=0)
                    
                    except BlockingIOError:
                        # No connection available yet, this is normal
                        pass
                    except Exception as e:
                        print(f"Error accepting client: {e}")
                
                # Check if both players are ready to start the game
                if not game_started and all(self.game_state["player_ready"]) and len(self.clients) == 2:
                    game_started = True
                    print("Both players are ready. Starting the game...")
                    self.initialize_game()
                
                # Check if the game is over
                if self.game_state.get("winner"):
                    time.sleep(5)  # Show winner for 5 seconds
                    self.running = False
                    break
                
                # Small delay to avoid high CPU usage
                time.sleep(0.1)
        
        except turtle.Terminator:
            pass  # Window was closed
        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            # Cleanup
            for client in self.clients:
                try:
                    client.close()
                except:
                    pass
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            print("Server shutting down")
    
    def handle_client(self, client_socket, player_num):
        """Handle messages from a client."""
        try:
            while self.running:
                try:
                    # Since socket is non-blocking, we need to handle BlockingIOError
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    
                    message = json.loads(data.decode())
                    message_type = message.get("type")
                    
                    if message_type == "ready":
                        with self.lock:
                            self.game_state["player_ready"][player_num] = True
                            self.client_names[player_num] = message.get("name", f"Player {player_num + 1}")
                        
                    elif message_type == "answer":
                        self.handle_answer(player_num, message.get("answer"))
                    
                    # Broadcast updated game state to all clients
                    self.broadcast_game_state()
                
                except BlockingIOError:
                    # This is normal for non-blocking sockets
                    time.sleep(0.1)
                    continue
                except json.JSONDecodeError:
                    print(f"Received invalid JSON from client {player_num}")
                    time.sleep(0.1)
                    continue
                except Exception as e:
                    print(f"Error processing message from client {player_num}: {e}")
                    break
                
        except Exception as e:
            print(f"Error handling client {player_num}: {e}")
        finally:
            print(f"Player {player_num + 1} disconnected")
            with self.lock:
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                    try:
                        client_socket.close()
                    except:
                        pass
    
    def broadcast_game_state(self):
        """Send the current game state to all connected clients."""
        with self.lock:
            state_copy = self.game_state.copy()
        
        message = json.dumps({
            "type": "game_state",
            "state": state_copy,
            "client_names": self.client_names
        })
        
        for client in self.clients:
            try:
                client.send(message.encode())
            except:
                pass  # Client might have disconnected
    
    def initialize_game(self):
        """Initialize the game state and UI on the server."""
        # Initialize game state
        with self.lock:
            self.game_state["game_started"] = True
            self.game_state["turn"] = 0
            self.game_state["winner"] = None
        
        # Setup visual display for server
        self.window = game_logic.setup_screen("Turtle Race with Quiz (Server)")
        self.red_turtle, self.blue_turtle = game_logic.init_turtles()
        game_logic.draw_finish_line()
        
        # Generate first question
        self.generate_new_question()
        self.broadcast_game_state()
    
    def generate_new_question(self):
        """Generate a new math question."""
        a, op, b = game_logic.generate_question()
        with self.lock:
            self.game_state["current_question"] = {"a": a, "op": op, "b": b}
    
    def handle_answer(self, player_num, answer):
        """Process a player's answer."""
        if player_num != self.game_state["turn"] % 2:
            return  # Not this player's turn
        
        current_question = self.game_state["current_question"]
        if not current_question:
            return
        
        a, op, b = current_question["a"], current_question["op"], current_question["b"]
        
        # Check if answer is correct
        is_correct = game_logic.check_answer(a, op, b, answer)
        
        with self.lock:
            # Move the turtle if answer is correct
            if is_correct:
                if player_num == 0 and self.red_turtle:  # Red player
                    game_logic.move_turtle(self.red_turtle)
                    if self.red_turtle:
                        self.game_state["red_pos"] = (self.red_turtle.xcor(), self.red_turtle.ycor())
                elif player_num == 1 and self.blue_turtle:  # Blue player
                    game_logic.move_turtle(self.blue_turtle)
                    if self.blue_turtle:
                        self.game_state["blue_pos"] = (self.blue_turtle.xcor(), self.blue_turtle.ycor())
            
            # Check for winner
            winner = None
            if self.red_turtle and game_logic.is_winner(self.red_turtle):
                winner = "red"
                self.game_state["winner"] = "red"
                game_logic.announce_winner("red")
            elif self.blue_turtle and game_logic.is_winner(self.blue_turtle):
                winner = "blue"
                self.game_state["winner"] = "blue"
                game_logic.announce_winner("blue")
            
            # Move to next turn if no winner
            if not winner:
                self.game_state["turn"] += 1
                self.generate_new_question()
    
    # No longer using these methods as they're covered by main_loop

if __name__ == "__main__":
    server = GameServer()
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("Server stopped by user")
