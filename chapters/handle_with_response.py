import socket

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)

    # Prepare an HTTP response
    response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello, World!</h1></body></html>"""
    client_socket.sendall(response.encode())
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Listening on port 8080...")

while True:
    client_socket, address = server_socket.accept()
    handle_request(client_socket)
