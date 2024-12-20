import socket

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)

    # Extracting the method and body
    method, path, _ = request.splitlines()[0].split()
    body = request.split("\r\n\r\n")[1] if method == "POST" else ""

    if method == "POST":
        response_body = f"<h1>POST Data Received:</h1><p>{body}</p>"
    else:
        response_body = "<h1>Welcome to the Home Page</h1>"

    response = (
        "HTTP/1.1 200 OK\n"
        "Content-Type: text/html\n"
        "\n"
        f"{response_body}"
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