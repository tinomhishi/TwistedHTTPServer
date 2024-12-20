import socket


def handle_request(client_socket):
    # Receive data from the client
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Listening on port 8080...")

while True:
    # Wait for a connection
    client_socket, address = server_socket.accept()
    print(f"Connection from {address}")
    handle_request(client_socket)
