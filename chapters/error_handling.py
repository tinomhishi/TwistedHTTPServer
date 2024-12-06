import socket

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    request_line = request.splitlines()[0]
    method, path, _ = request_line.split()

    if path == '/':
        body = "<h1>Welcome to the Home Page</h1>"
        status = "200 OK"
    elif path == '/hello':
        body = "<h1>Hello, User!</h1>"
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
