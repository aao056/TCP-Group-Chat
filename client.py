import socket
import threading


# FEEL FREE TO CHANGE THE NUMBER OF THE PORT AS IT IS CONVENIENT
PORT = 55999

# Getting the localhost
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER,PORT)


class Client:
    # Starting the client service
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    def __init__(self,username):
        # Sending the username to the server and ask for permission to join
        self.username = username
        self.client.send(username.encode('ascii'))
        response = self.client.recv(1024).decode('ascii')
        # If the username is taken or forbidden it will deny the permission
        # A message will be displayed in order to warn the client to try to join with a different nickname
        # The process will be repeated until the client enters with a nickname which satisfies the conditions
        while response == 'taken' or response == 'forbidden':
            if response == 'taken':
                print(f'{self.username} already exists.')
            if response == 'forbidden':
                print(f'Your username has forbidden characters')
            self.username = input('Choose a different username: ')
            self.client.send(self.username.encode('ascii'))
            response = self.client.recv(1024).decode('ascii')

    def listen(self):
        while True:
            # Listening thread from messages from the server and display them
            try:
                message = self.client.recv(1024).decode('ascii')
                print(message)
            # If an error occurs the client will be closed
            except:
                print("Oops.. there has been an issue.Disconnected from the server.")
                self.client.close()
                break

    def write(self):
        # Writing thread which takes input from client keyboard and send it to the server
        while True:
            try:
                message = f'{self.username}: {input("")}'
                self.client.send(message.encode('ascii'))
                # If an error occurs the client will be closed
            except:
                print("Oops.. there has been an issue.Disconnected from the server.")
                self.client.close()
                break


if __name__ == '__main__':
    nickname = input('Choose a nickname: ')
    client = Client(nickname)
    listen = threading.Thread(target=client.listen)
    write = threading.Thread(target=client.write)
    listen.start()
    write.start()
