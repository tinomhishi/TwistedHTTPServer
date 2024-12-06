import socket
import threading

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)
    response = (
        "HTTP/1.1 200 OK\n"
        "Content-Type: text/html\n"
        "\n"
        "<html><body><h1>Hello, World!</h1></body></html>"
    )
    client_socket.sendall(response.encode())
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(5)
print("Listening on port 8080...")

while True:
    client_socket, addr = server_socket.accept()
    thread = threading.Thread(target=handle_request, args=(client_socket,))
    thread.start()
