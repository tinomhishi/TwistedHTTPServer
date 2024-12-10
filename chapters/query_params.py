import socket
from urllib.parse import parse_qs, urlparse

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)

    method, path, _ = request.splitlines()[0].split()
    parsed_url = urlparse(path)
    query_params = parse_qs(parsed_url.query)

    response_body = f"<h1>Query Parameters</h1><pre>Mame: {query_params.get('name')}</pre>"
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
