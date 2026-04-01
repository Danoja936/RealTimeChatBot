import socket
import threading
import json
from chatbot import chatbot_response

HOST = '0.0.0.0'
PORT = 5566

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()


clients = {}

def send_json(client_socket, sender, message_type, content):
    """Utility to send structured JSON data to a client"""
    packet = {
        "sender": sender,
        "type": message_type,
        "content": content
    }
    try:
        client_socket.send(json.dumps(packet).encode())
    except:
        pass

def broadcast(packet, exclude_sender=None):
    """Broadcasting structured JSON packets"""
    for client_socket in clients:
        if client_socket != exclude_sender:
            try:
                client_socket.send(json.dumps(packet).encode())
            except:
                continue

def handle_client(client):
    nickname = "Guest"
    try:
       
        initial_msg = client.recv(1024).decode()
        data = json.loads(initial_msg)
        nickname = data.get("content", "Guest")
        clients[client] = nickname
        
        print(f"Server: {nickname} joined.")
        broadcast({"sender": "Server", "type": "info", "content": f"{nickname} joined the chat!"}, exclude_sender=client)
        send_json(client, "Server", "info", f"Welcome {nickname}! Type /list for users, /pm <user> <msg> for private chat.")

        while True:
       
            message = client.recv(1024).decode()
            if not message:
                break

            data = json.loads(message)
            msg_content = data.get("content", "")

            if msg_content.startswith("/"):
                handle_command(client, nickname, msg_content)
            else:

                print(f"[{nickname}]: {msg_content}")
                broadcast({"sender": nickname, "type": "chat", "content": msg_content}, exclude_sender=client)
       
                bot_reply = chatbot_response(msg_content)
                send_json(client, "Bot", "chat", bot_reply)

    except Exception as e:
        print(f"Error handling {nickname}: {e}")
    finally:
        if client in clients:
            left_nickname = clients[client]
            del clients[client]
            client.close()
            broadcast({"sender": "Server", "type": "info", "content": f"{left_nickname} left the chat."}, exclude_sender=None)
            print(f"Server: {left_nickname} disconnected.")

def handle_command(client, sender_nick, command_str):
    parts = command_str.split(" ", 2)
    cmd = parts[0].lower()

    if cmd == "/list":
        user_list = ", ".join(clients.values())
        send_json(client, "Server", "info", f"Connected users: {user_list}")
    
    elif cmd == "/pm" and len(parts) > 2:
        target_nick = parts[1]
        content = parts[2]
        found = False
        for sock, nick in clients.items():
            if nick == target_nick:
                send_json(sock, f"PM from {sender_nick}", "private", content)
                found = True
                break
        if not found:
            send_json(client, "Server", "error", f"User {target_nick} not found.")
            
    else:
        send_json(client, "Server", "error", "Unknown command or missing arguments.")

print("Server is running...")
while True:
    client, addr = server.accept()
    print(f"Connected with {addr}")
    threading.Thread(target=handle_client, args=(client,)).start()
