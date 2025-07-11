from socket import *
import ssl
import os
import base64
import getpass

# Message content
msg = "\r\nI love computer networks!\r\n"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
smtp_port = int(os.getenv('SMTP_PORT', '587'))
mailserver = (smtp_host, smtp_port)

# Credentials
username = os.getenv('SMTP_USER', 'oishani.ganguly@gmail.com')
password = os.getenv('SMTP_PASS') or getpass.getpass('SMTP password: ')

# Sender and recipient
sender = username
recipient = os.getenv('SMTP_RECIPIENT', 'oishani.ganguly@gmail.com')

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

# Receive server greeting
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response
heloCommand = f'HELO {os.uname()[1]}\r\n'
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')

# EHLO and STARTTLS
clientSocket.send(f'EHLO {os.uname()[1]}\r\n'.encode())
print(clientSocket.recv(1024).decode())
clientSocket.send(b'STARTTLS\r\n')
print(clientSocket.recv(1024).decode())
clientSocket = ssl.wrap_socket(clientSocket)
clientSocket.send(f'EHLO {os.uname()[1]}\r\n'.encode())
print(clientSocket.recv(1024).decode())

# Authenticate with AUTH LOGIN
clientSocket.send(b'AUTH LOGIN\r\n')
print(clientSocket.recv(1024).decode())
clientSocket.send(base64.b64encode(username.encode()) + b'\r\n')
print(clientSocket.recv(1024).decode())
clientSocket.send(base64.b64encode(password.encode()) + b'\r\n')
print(clientSocket.recv(1024).decode())

# Send MAIL FROM command and print server response.
clientSocket.send(f'MAIL FROM:<{sender}>\r\n'.encode())
print(clientSocket.recv(1024).decode())

# Send RCPT TO command and print server response.
clientSocket.send(f'RCPT TO:<{recipient}>\r\n'.encode())
print(clientSocket.recv(1024).decode())

# Send DATA command and print server response.
clientSocket.send(b'DATA\r\n')
print(clientSocket.recv(1024).decode())

# Send message data.
clientSocket.send(msg.encode())

# Message ends with a single period.
clientSocket.send(endmsg.encode())
print(clientSocket.recv(1024).decode())

# Send QUIT command and get server response.
clientSocket.send(b'QUIT\r\n')
print(clientSocket.recv(1024).decode())

# Close connection
clientSocket.close()
