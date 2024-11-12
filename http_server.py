import json

from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.web.static import File
from twisted.internet.task import deferLater
from twisted.web.server import NOT_DONE_YET
from twisted.web._responses import FORBIDDEN, NOT_FOUND


class HTTPServer(Resource):
    def getChild(self, path, request):
        if path == b"hello":
            return self.HelloEndpoint()
        elif path == b"echo":
            return self.EchoEndpoint()
        elif path == b"headers":
            return self.HeaderEndpoint()
        elif path == b"json":
            return self.JsonEndpoint()
        elif path == b"status":
            return self.StatusCodeEndpoint()
        elif path == b"query":
            return self.QueryParamEndpoint()
        elif path == b"stream":
            return self.StreamingEndpoint()
        elif path == b"static":
            return File("./public")
        return NOT_FOUND

    class HelloEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            return b"Hello, World!"
        
    class EchoEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            message = request.args.get(b"message", [b"No message"])[0]
            return b"Echo: " + message
    
    class HeaderEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            # Attempt to get the value of 'X-Custom-Header' from the incoming request
            custom_header_value = request.getHeader(b"X-Custom-Header")
            
            if custom_header_value:
                # Respond with the value of the header if it was provided
                response = f"Received X-Custom-Header: {custom_header_value}".encode()
            else:
                # Indicate that the header was not provided
                response = b"X-Custom-Header not provided in the request."
                
            return response
        
    class JsonEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            data = {"message": "Hello, JSON!"}
            request.setHeader(b"content-type", b"application/json")
            return json.dumps(data).encode()

        def render_POST(self, request):
            raw_data = request.content.read()
            try:
                json_data = json.loads(raw_data)
                response = json.dumps({"echo": json_data}).encode()
            except json.JSONDecodeError:
                response = b"Invalid JSON data received."

            return response
    
    class StatusCodeEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            request.setResponseCode(404)
            return NOT_FOUND
    
    class QueryParamEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):
            name = request.args.get(b"name", [b"Anonymous"])[0].decode()
            age = request.args.get(b"age", [b"Unknown"])[0].decode()
            return f"Name: {name}, Age: {age}".encode()
    
    class StaticFileServer(Resource):
        # isLeaf = True
        def init__(self):
            super().__init()
            self.putChild(b"public", File("./public"))
    
    class StreamingEndpoint(Resource):
        isLeaf = True
        def render_GET(self, request):

           request.setHeader(b"content-type", b"text/plain")
           request.write(b"Starting data stream...\n")
           self.send_chunk(request, 1)
           return NOT_DONE_YET
    
        def send_chunk(self, request, count):
           if count > 5:
               request.finish()
               return
           request.write(f"Chunk {count}\n".encode())
           deferLater(reactor, 1, self.send_chunk, request, count + 1)
        
root = HTTPServer()
factory = Site(root)
reactor.listenTCP(8080, factory)
reactor.run()