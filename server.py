import socket
import threading
from chatbot import chatbot_response

HOST = '127.0.0.1'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []

def broadcast(message, sender):
    for client in clients:
        if client != sender:
            client.send(message.encode())

def handle_client(client):
    while True:
        try:
            # Receive message from client
            message = client.recv(1024).decode()
            if not message:
                break

            print(f"Received: {message}")  # For debugging

            # Broadcast to other clients
            broadcast(f"User: {message}", client)

            # Send chatbot reply back to **sender**
            bot_reply = chatbot_response(message)
            client.send(f"Bot: {bot_reply}".encode())

        except:
            clients.remove(client)
            client.close()
            break

print("Server is running...")
while True:
    client, addr = server.accept()
    print(f"Connected with {addr}")
    clients.append(client)
    threading.Thread(target=handle_client, args=(client,)).start()
