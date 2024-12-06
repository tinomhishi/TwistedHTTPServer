import socket

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a port
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Listening on port 8080...")

while True:
    # Wait for a client to connect
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}")
    client_socket.close()