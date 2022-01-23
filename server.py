import socket
import threading
import time
import hashlib
import re

# FEEL FREE TO CHANGE THE NUMBER OF THE PORT AS IT IS CONVENIENT
PORT = 55999

# Getting the localhost
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

# Creating and initializing the server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

# Keeping track of the clients connected and their usernames
clients = []
nicknames = []
nicknames_clients_dict = {}
# List of forbidden characters in order to prevent users to use them in their nicknames
FORBIDDEN_CHARACTERS = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', ' ', '<',
                        '`', '}', '.', '_', '=', ']', '!', '>', ';', '?', '#', '$', ')', '/'}

# Regex in order to recognize special commands from the user
TIME_PATTERN = r'(\w+): --t'
ENCRYPT_PATTERN = r'(\w+): (\w+) --h (\w+)'
LIST_CLIENTS_PATTERN = r'(\w+): --l'

class Server:
    def __init__(self):
        while True:
            # Get the client data
            self.client, addr = server.accept()
            nickname = self.client.recv(1024).decode('ascii')
            while True:
                # Check if there is other client on the server with the username they sent
                # If there is a match ask them to send another username
                if nickname in nicknames:
                    self.client.send('taken'.encode('ascii'))
                    nickname = self.client.recv(1024).decode('ascii')

                # Check if the username they sent has forbidden characters
                # If there is a match ask them to send another username
                elif any(letter in nickname for letter in FORBIDDEN_CHARACTERS):
                    self.client.send('forbidden'.encode('ascii'))
                    nickname = self.client.recv(1024).decode('ascii')

                # Otherwise allow them to join the server and collect their data in the clients list
                else:
                    self.client.send('Connected to server'.encode('ascii'))
                    self.time_start = time.time()
                    nicknames.append(nickname)
                    clients.append(self.client)
                    nicknames_clients_dict[nickname] = self.client
                    self.handle_message(f'{nickname} has joined the server.There are {len(clients)} active clients.'.encode('ascii'))
                    break

            # In order to have concurrency a thread to handle each client is created and started
            thread = threading.Thread(target=self.handle_client, args=(self.client,))
            thread.start()

    def handle_message(self, message):
        # Checking if the user sent the time command (--t) and tell them how many seconds they spent on the chat
        # (rounded to 4 decimals)
        if re.match(TIME_PATTERN,message.decode('ascii')):
            time_on_server = time.time() - self.time_start
            user_to_display = re.match(TIME_PATTERN,message.decode('ascii')).group(1)
            nicknames_clients_dict[user_to_display].send(f'You spent currently on the server {round(time_on_server,4)} seconds'.encode('ascii'))
        # Checking if the user wants to hide a message from another user (--h NAME_OF_USER)
        # The message wil get encrypted using sha256 algorithm and will be displayed to the user mentioned --h
        # If the user enters a name which is not on the chat,no encryption will happen,it will act like the base case
        elif re.match(ENCRYPT_PATTERN, message.decode('ascii')):
            sender_of_encrypted = re.match(ENCRYPT_PATTERN, message.decode('ascii')).group(1)
            message_to_encrypt = re.match(ENCRYPT_PATTERN, message.decode('ascii')).group(2)
            hide_the_message_from = re.match(ENCRYPT_PATTERN, message.decode('ascii')).group(3)
            for nickname in nicknames:
                if nickname == hide_the_message_from:
                    encrypted_message = sender_of_encrypted + ': ' + hashlib.sha256(
                        message_to_encrypt.encode()).hexdigest()
                    nicknames_clients_dict[nickname].send(encrypted_message.encode())
                else:
                    nicknames_clients_dict[nickname].send(message)
        # Checking if the user sent the list clients command (--l) and showing them the nicknames of the group users
        elif re.match(LIST_CLIENTS_PATTERN, message.decode('ascii')):
            user_to_display = re.match(LIST_CLIENTS_PATTERN, message.decode('ascii')).group(1)
            nicknames_clients_dict[user_to_display].send(f'Active clients nicknames are: {nicknames}'.encode('ascii'))
        # Default case when the user did not send any special commands
        # In this case just broadcast their message to the group
        else:
            for client in clients:
                client.send(message)


    def handle_client(self, client):
        while True:
            # Listening to the client messages and handle them
            try:
                message = client.recv(1024)
                self.handle_message(message)
            # If there are any errors ocurring while handling a client just close the connection
            # They will be removed from the clients and nickname lists in order to prevent bugs
            # A message will be broadcasted to the server informing them that the user left the chat
            except:
                index = clients.index(client)
                nickname = nicknames[index]
                nicknames.remove(nickname)
                clients.remove(client)
                self.handle_message(f'{nickname} has left the chat'.encode())
                client.close()
                break

# Starting the server and waiting for clients
if __name__ == '__main__':
    server = Server()
