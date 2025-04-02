from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import hashlib

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

client_key=RSA.generate(2048)
server_public_key=RSA.import_key(client_socket.recv(2048))
client_socket.send(client_key.publickey().export_key(format='PEM'))
encrypted_aes_key=client_socket.recv(2048)
cipher_rsa=PKCS1_OAEP.new(client_key)
aes_key=cipher_rsa.decrypt(encrypted_aes_key)
def encrypt_message(message, key):
    cipher=AES.new(key, AES.MODE_CBC)
    ciphertext=cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv+ciphertext
def decrypt_message(encrypted_message, key):
    iv=encrypted_message[:AES.block_size]
    ciphertext=encrypted_message[AES.block_size:]
    cipher=AES.new(key, AES.MODE_CBC, iv)
    decrypted_message=unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()
def receive_messages():
    while True:
        encrypted_message=client_socket.recv(1024)
        decrypted_message=decrypt_message(encrypted_message, aes_key)
        print("Received message:", decrypted_message)
        receive_thread=threading.Thread(target=receive_messages)
        receive_thread.start()
while True:
    message=input("Enter message:('exit' to quit)")
    encrypted_message=encrypt_message(message, aes_key)
    client_socket.send(encrypted_message)
    if message=='exit':
        break
        
client_socket.close()