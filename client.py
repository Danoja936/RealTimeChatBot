import socket
import threading
import json
import sys


BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Ask the user which server IP to connect to (server laptop's IP on the same network)
server_ip = input("Enter server IP (e.g. 192.168.1.5): ").strip() or '127.0.0.1'

try:
    client.connect((server_ip, 5566))
except:
    print(f"{RED}Error: Could not connect to server at {server_ip}:5566!{RESET}")
    sys.exit()

nickname = input("Choose your nickname: ")

def send_packet(client_socket, sender, msg_type, content):
    packet = {"sender": sender, "type": msg_type, "content": content}
    client_socket.send(json.dumps(packet).encode())


send_packet(client, nickname, "join", nickname)

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            
            data = json.loads(message)
            sender = data.get("sender")
            content = data.get("content")
            msg_type = data.get("type")

            
            if msg_type == "info":
                print(f"{YELLOW}[SYSTEM] {content}{RESET}")
            elif msg_type == "private":
                print(f"{BLUE}[PM] {sender}: {content}{RESET}")
            elif msg_type == "error":
                print(f"{RED}[ERROR] {content}{RESET}")
            elif sender == "Bot":
                print(f"{GREEN}[BOT]: {content}{RESET}")
            else:
                print(f"{sender}: {content}")

        except:
            print(f"{RED}Connection closed.{RESET}")
            break

def send():
    while True:
        try:
            msg = input()
            if not msg: continue
            
          
            send_packet(client, nickname, "chat", msg)
            
            if msg.lower() == "/quit":
                client.close()
                break
        except:
            break

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

send()
