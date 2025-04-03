import socket
import ssl
import threading

server_address = ('localhost', 12345)

def receive_data(ssl_socket):
    while True:
        data = ssl_socket.recv(1024)
        if not data:
            break
        print("Nhận:", data.decode('utf-8'))

# Tạo client SSL
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.verify_mode = ssl.CERT_NONE

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')
ssl_socket.connect(server_address)

receive_thread = threading.Thread(target=receive_data, args=(ssl_socket,))
receive_thread.start()

while True:
    message = input("Nhập tin nhắn: ")
    ssl_socket.send(message.encode('utf-8'))