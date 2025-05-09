import socket
import threading
import random
import json
import time

# Game settings
SCREEN_X = 500
SCREEN_Y = 400
WIN_X = SCREEN_X // 2 - 20

# Server settings
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 5678
MAX_PLAYERS = 4
COLORS = ["red", "blue", "green", "purple"]

class GameServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(MAX_PLAYERS)
        
        self.clients = []
        self.player_positions = {}  # {client_id: (x, y)}
        self.player_colors = {}     # {client_id: color}
        self.player_names = {}      # {client_id: name}
        self.game_started = False
        self.current_turn = 0
        self.winner = None
        
        print(f"Server started on {HOST}:{PORT}")
    
    def generate_question(self):
        """Generate a random math question"""
        op = random.choice(['+', '-', '*', '/'])
        if op == '/':
            # Integer division facilitator
            b = random.randint(1, 10)
            a = b * random.randint(0, 10)
        else:
            a = random.randint(0, 30)
            b = random.randint(0, 30)
        
        # Calculate answer
        if op == '+':
            correct = a + b
        elif op == '-':
            correct = a - b
        elif op == '*':
            correct = a * b
        else:
            correct = a // b
            
        return {"a": a, "op": op, "b": b, "correct": correct}
    
    def broadcast(self, message):
        """Send message to all connected clients"""
        for client in self.clients:
            try:
                client.send(json.dumps(message).encode('utf-8'))
            except:
                # Remove client if can't send
                self.clients.remove(client)
    
    def handle_client(self, client_socket, client_id):
        """Handle communication with a client"""
        try:
            # Wait for player name
            data = client_socket.recv(1024).decode('utf-8')
            player_data = json.loads(data)
            player_name = player_data.get('name', f"Player {client_id}")
            self.player_names[client_id] = player_name
            
            # Assign color and initial position
            color = COLORS[client_id % len(COLORS)]
            self.player_colors[client_id] = color
            y_pos = 50 - client_id * 40  # Vertical spacing between turtles
            self.player_positions[client_id] = (-SCREEN_X // 2 + 20, y_pos)
            
            # Send initial game state to new client
            self.send_game_state(client_socket)
            
            # Broadcast new player joined
            self.broadcast({
                "type": "player_joined",
                "id": client_id,
                "name": player_name,
                "color": color,
                "position": self.player_positions[client_id]
            })
            
            # Start game when we have at least 2 players
            if len(self.clients) >= 2 and not self.game_started:
                time.sleep(2)  # Brief delay before starting
                self.start_game()
            
            # Main communication loop
            while True:
                if client_socket not in self.clients:
                    break
                    
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                    
                message = json.loads(data)
                self.process_message(message, client_id)
                
        except Exception as e:
            print(f"Error with client {client_id}: {e}")
        finally:
            # Clean up when client disconnects
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            if client_id in self.player_positions:
                del self.player_positions[client_id]
            if client_id in self.player_colors:
                del self.player_colors[client_id]
            if client_id in self.player_names:
                del self.player_names[client_id]
            client_socket.close()
            
            # Broadcast player left
            self.broadcast({
                "type": "player_left",
                "id": client_id
            })
    
    def process_message(self, message, client_id):
        """Process messages from clients"""
        msg_type = message.get('type')
        
        if msg_type == 'answer':
            # Only process answer if it's this player's turn
            if self.game_started and self.current_turn == client_id:
                answer = message.get('answer')
                question = message.get('question')
                correct_answer = question.get('correct')
                
                is_correct = (answer == correct_answer)
                
                if is_correct:
                    # Move player forward
                    x, y = self.player_positions[client_id]
                    x += 20  # Move 20 units forward
                    self.player_positions[client_id] = (x, y)
                    
                    # Check for winner
                    if x >= WIN_X:
                        self.winner = client_id
                        self.game_started = False
                        self.broadcast({
                            "type": "game_over",
                            "winner": {
                                "id": client_id,
                                "name": self.player_names[client_id],
                                "color": self.player_colors[client_id]
                            }
                        })
                    else:
                        # Update all clients with new position
                        self.broadcast({
                            "type": "player_moved",
                            "id": client_id,
                            "position": self.player_positions[client_id],
                            "correct": True
                        })
                else:
                    # Inform about wrong answer
                    self.broadcast({
                        "type": "player_moved",
                        "id": client_id,
                        "position": self.player_positions[client_id],
                        "correct": False
                    })
                
                # Move to next player's turn
                self.next_turn()
    
    def next_turn(self):
        """Move to the next player's turn"""
        # Find next valid player
        player_ids = list(self.player_positions.keys())
        if not player_ids:
            return
            
        # Sort to ensure consistent order
        player_ids.sort()
        
        # Find index of current player
        try:
            current_index = player_ids.index(self.current_turn)
            next_index = (current_index + 1) % len(player_ids)
        except ValueError:
            next_index = 0
            
        self.current_turn = player_ids[next_index]
        
        # Generate question for next player
        question = self.generate_question()
        
        # Send turn notification
        self.broadcast({
            "type": "next_turn",
            "player_id": self.current_turn,
            "question": question
        })
    
    def send_game_state(self, client_socket):
        """Send current game state to a client"""
        game_state = {
            "type": "game_state",
            "players": {},
            "game_started": self.game_started,
            "current_turn": self.current_turn if self.game_started else None,
            "winner": self.winner
        }
        
        # Add all players' info
        for player_id in self.player_positions:
            game_state["players"][player_id] = {
                "name": self.player_names[player_id],
                "color": self.player_colors[player_id],
                "position": self.player_positions[player_id]
            }
        
        client_socket.send(json.dumps(game_state).encode('utf-8'))
    
    def start_game(self):
        """Start the game"""
        self.game_started = True
        self.current_turn = list(self.player_positions.keys())[0]  # First player starts
        
        # Broadcast game start
        self.broadcast({
            "type": "game_started",
        })
        
        # Send first question
        question = self.generate_question()
        self.broadcast({
            "type": "next_turn",
            "player_id": self.current_turn,
            "question": question
        })
    
    def accept_connections(self):
        """Accept new client connections"""
        client_id = 0
        
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"New connection from {addr}")
            
            # Add to client list
            self.clients.append(client_socket)
            
            # Start thread to handle this client
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id))
            client_thread.daemon = True
            client_thread.start()
            
            client_id += 1
    
    def run(self):
        """Run the server"""
        try:
            self.accept_connections()
        except KeyboardInterrupt:
            print("Server shutting down...")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    server = GameServer()
    server.run()