import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path.lstrip('/')
        
        # Define different endpoints
        if path == "hello":
            self.hello_endpoint()
        elif path == "echo":
            self.echo_endpoint()
        elif path == "headers":
            self.header_endpoint()
        elif path == "json":
            self.json_endpoint()
        elif path == "status":
            self.status_code_endpoint()
        elif path == "query":
            self.query_param_endpoint()
        elif path == "stream":
            self.streaming_endpoint()
        elif path == "static":
            self.static_file_endpoint(parsed_path.path)
        else:
            self.send_error(404, "Endpoint not found")

    def hello_endpoint(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

    def echo_endpoint(self):
        message = parse_qs(urlparse(self.path).query).get('message', ["No message"])[0]
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Echo: " + message.encode())

    def header_endpoint(self):
        custom_header_value = self.headers.get("X-Custom-Header")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        if custom_header_value:
            self.wfile.write(f"Received X-Custom-Header: {custom_header_value}".encode())
        else:
            self.wfile.write(b"X-Custom-Header not provided in the request.")

    def json_endpoint(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        data = {"message": "Hello, JSON!"}
        self.wfile.write(json.dumps(data).encode())

    def status_code_endpoint(self):
        self.send_response(404)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Not Found")

    def query_param_endpoint(self):
        params = parse_qs(urlparse(self.path).query)
        name = params.get("name", ["Anonymous"])[0]
        age = params.get("age", ["Unknown"])[0]
        response = f"Name: {name}, Age: {age}"
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

    def static_file_endpoint(self, path):
        # Serve a static file, e.g., from "./public"
        try:
            with open(f".{path}", "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def streaming_endpoint(self):
        # Streaming is complex in synchronous servers; here, we'll send chunks sequentially
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        
        for count in range(1, 6):
            self.wfile.write(f"Chunk {count}\n".encode())
            self.wfile.flush()

def run(server_class=HTTPServer, handler_class=MyHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting httpd server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
