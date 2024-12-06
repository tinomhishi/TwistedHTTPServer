import socket
import os

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)

    method, path, _ = request.splitlines()[0].split()

    if path == "/":
        path = "/pages/index.html"

    file_path = f".{path}"
    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, "r") as file:
            body = file.read()
        status = "200 OK"
    else:
        body = "<h1>404 Not Found</h1>"
        status = "404 Not Found"

    response = (
        f"HTTP/1.1 {status}\n"
        "Content-Type: text/html\n"
        "\n"
        f"{body}"
    )
    client_socket.sendall(response.encode())
    client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Listening on port 8080...")

while True:
    client_socket, address = server_socket.accept()
    handle_request(client_socket)
