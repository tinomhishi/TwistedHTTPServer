# TwistedHTTPServer# HTTP From Scratch With Python
HTTP (Hypertext Transfer Protocol) is an application layer protocol the defines the standard for communication between web browsers and web servers in a client server architecture. The application layer is responsible for providing network services directly to end-user applications, enabling communication between client and server through protocols that facilitate data exchange, such as HTTP, FTP, and SMTP.


![OSI 7 layers](https://www.imperva.com/learn/wp-content/uploads/sites/13/2020/02/OSI-7-layers.jpg.webp)



## 1. Setting up a basic socket.

A socket is bidirectional structure that facilitates communication between two programs. Below we are setting up a basic TCP server that listens on port 8080 for incoming connections. Python’s socket module facilitates communication with low-level networking interfaces. 

```
    # A simple TCP server using the socket module
    import socket
    
    ''' 
    import the socket module, which facilitates access to the BSD socket interface. Berkley Socket API that allows us to add internet communication to Python Applications. It allows for network communication using various protocols, including TCP and UDP.
    '''
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF_INET that the socket will use IPv4 addressing
    # Specifying that the socket will use TCP (Transmission Control Protocol), which is a connection-oriented protocol that ensures reliable communication.
    
    server_socket.bind(('localhost', 8080))
    # Binding the socket with a specific address and port number:
    server_socket.listen(1)
    # Enables the server to accept incoming connections. The arg 1 specifies the maximum number of queued connections (i.e., how many clients can wait to connect while the server is busy)
    print("Listening on port 8080...")
    
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        client_socket.close() 
``````

## 2. Handle Request

The next step is to handle the connection event. We will now log a connection event. 

```
    import socket
    
    
    def handle_request(client_socket):
        # Receive data from the client
        request = client_socket.recv(1024).decode()
        # Method reads up to 1024 bytes from the socket
        print("Request received:\n", request)
        client_socket.close()
        # Closing the socket connection to free up resources
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Listening on port 8080...")
    
    while True:
        # Wait for a connection
        client_socket, address = server_socket.accept()
        print(f"Connection from {address}")
        handle_request(client_socket)
    
```


## 3. Handle with response

At this point all of our server versions have not been returning responses. Below we are returning a string with HTML.

```
    import socket
    
    
    def handle_request(client_socket):
        request = client_socket.recv(1024).decode()
        print("Request received:\n", request)
        # Prepare an HTTP response
        response = (
            "HTTP/1.1 200 OK\n"
            "Content-Type: text/html\n"
            "\n"
            "<html><body><h1>Hello, World!</h1></body></html>"
        )
        # Response tuple "HTTP/1.1 200 OK" indicates successful request
        # Specifying the response is in html
        # HTML Content
        client_socket.sendall(response.encode())
        # encoding response into bytes then sending over socket
        client_socket.close()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)
    print("Listening on port 8080...")
    
    while True:
        client_socket, address = server_socket.accept()
        handle_request(client_socket)
```


## 4. Routing
    import socket
    
```
    def handle_request(client_socket):
        request = client_socket.recv(1024).decode()
        print("Request received:\n", request)
        # Parse the request line
        request_line = request.splitlines()[0]
        # Extract first line from request.
        # Contains Method GET and path
        method, path, _ = request_line.split()
        
        # Determine response based on the path
        # Generating response based on path
        if path == '/':
            body = "<h1>Welcome to the Home Page</h1>"
        elif path == '/hello':
            body = "<h1>Hello, User!</h1>"
        else:
            body = "<h1>404 Not Found</h1>"
        response = (
            "HTTP/1.1 200 OK\n"
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
    
```

## 5. Error Handling

Below is an updated version making use of status codes and returning them in our response.

```
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
    
```

## 5. Concurrency

We can give the server the capability to handle multiple concurrent connections using Python’s thread module. In the example below each new connection will spin a new thread to process the new incoming request.

```

    import socket
    import threading
    # Threading module for us to manage requests with threads, enabling the server to handle multiple clients concurrently.
    
    
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
    # We increase the number of queued connections
    print("Listening on port 8080...")
    while True:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=handle_request, args=(client_socket,))
        # target specifies the function to run in the thread
        # args tuple of args to be send to the request
        # starting our thread
        thread.start()
    
```

**Bench Marking**
This small change can be illustrated using any earlier version of our basic server and running the script below to make multiple connections to our server. We can use tools for testing the performance of this iteration of the server with tools like Apache Benchmark.




## 6. Handling Post Requests

We use the line split `request.splitlines()[0].split()` to get our request method. The traverse the request to where the payload it and echo it back in our response. The positions of headers and payloads are stipulated in the protocol https://datatracker.ietf.org/doc/html/rfc7230

```

    import socket
    
    def handle_request(client_socket):
        request = client_socket.recv(1024).decode()
        print("Request received:\n", request)
        # Extracting the method and body
        method, path, _ = request.splitlines()[0].split()
        body = request.split("\r\n\r\n")[1] if method == "POST" else ""
        # The post payload will appear after the headers
        # The separation between the headers and the payload is
        # by Carriage Return Line Feed
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

```
## 7. Serve Static

We can modify our server to serve static files from a local file system as we have done below. In our url we need reference the file path. http://localhost:8080/chapters/pages/index.html

```

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
    


## Query Parameters

We can use the predictability of the HTTP standard protocols to extract URL parameters. We will continue to use the python standard library, this time `urllib` to parse the string into a dictionary.

```
    import socket
    from urllib.parse import parse_qs, urlparse
    
    
    def handle_request(client_socket):
        request = client_socket.recv(1024).decode()
        print("Request received:\n", request)
        method, path, _ = request.splitlines()[0].split()
        parsed_url = urlparse(path)
        # urlparse Splits down a URL into its components
        # ETC path, query
        query_params = parse_qs(parsed_url.query)
       # Converts parameters in a URL into a dictionary-like object
    
        response_body = f"<h1>Query Parameters</h1><pre>{query_params}</pre>"
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
    


## Reasons to understand lower-level basics of HTTP
- Enhances our ability to develop well designed API endpoints for integration.
- Efficient Debugging of network disruptions.
- Improved understanding of Protocols and how they work.
- Improved Front End development by improving our understanding of how browsers interact with server.
- Improving knowledge of Debugging tools. Postman, Apache bench marking.


https://github.com/tinomhishi/TwistedHTTPServer


Further Reading

https://docs.python.org/3/library/socket.html#

