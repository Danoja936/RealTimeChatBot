import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message:
                print(message)
        except:
            print("Connection closed.")
            break

def send():
    while True:
        try:
            message = input()
            client.send(message.encode())
        except:
            break

threading.Thread(target=receive, daemon=True).start()
send()
