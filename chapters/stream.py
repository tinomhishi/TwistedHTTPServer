import os
import socket
import mimetypes

def handle_request(client_socket):
    request = client_socket.recv(1024).decode()
    print("Request received:\n", request)

    try:
        method, path, _ = request.splitlines()[0].split()
        if path == "/":
            path = "/chapters/media/guy_riding_horse.mp4"

        file_path = f".{path}"
        print(f'>>>>>>>>> {os.path.exists(file_path)}')
        print(f'>>>>>>>>> {os.path.exists(path)}')
        print(f'>>>>>>>>> {os.getcwd()}')
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Determine the file's MIME type
            mime_type, _ = mimetypes.guess_type(file_path)

            if not mime_type:
                mime_type = "application/octet-stream"

            # Send response headers
            response_headers = (
                "HTTP/1.1 200 OK\n"
                f"Content-Type: {mime_type}\n"
                "Connection: close\n"
                "\n"
            )
            client_socket.sendall(response_headers.encode())

            # Stream the file in chunks
            with open(file_path, "rb") as file:
                while chunk := file.read(4096):  # 4KB chunks
                    client_socket.sendall(chunk)
        else:
            # File not found
            response = (
                "HTTP/1.1 404 Not Found\n"
                "Content-Type: text/html\n"
                "\n"
                "<h1>404 Not Found</h1>"
            )
            client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error: {e}")
        response = (
            "HTTP/1.1 500 Internal Server Error\n"
            "Content-Type: text/html\n"
            "\n"
            "<h1>500 Internal Server Error</h1>"
        )
        client_socket.sendall(response.encode())

    finally:
        client_socket.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)
print("Listening on port 8080...")

while True:
    client_socket, address = server_socket.accept()
    handle_request(client_socket)
