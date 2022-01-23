# TCP-Group-Chat
TCP group chat with possibility to encrypt a message and hiding it from an user by typing a command
# How to use it?
Clone this repo , open a command line and run the server from the terminal (python server.py) and after that open as more terminal windows as you like and run them in the same way (python client.py). If done right it should ask you for a username to join the chat,enter any name you like but do not use any special characters.
Now you should be able to have a local group chat,try to send a few messages and see if they are displayed on each window

# How to use the special commands in the chat?
If you want to see how many seconds you spent connected to the server , type --t in the chat and hit enter.
If you want to see a list with the active clients connected , type --l in the chat and hit enter. You should be able to see a list with all the usernames connected.
If you want to hide a message from a particular user , you want all the users but except one to see a message you can do it with using --h command. Type [message] --h [name of the user you do not want to see your message] and hit enter.

Example: Hello? --h John

Instead of Hello , John will see a sha256 key and will not be able to read Hello from it.For other users it will be displayed as a normal message.
# Errors when running the script
If you got an error when running any of those 2 scripts, most probably you should change the number of the port. 
