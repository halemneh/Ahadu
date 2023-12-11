from http.server import HTTPServer, BaseHTTPRequestHandler

class requestHandler(BaseHTTPRequestHandler):
    def do_get(self):
        self.send_response(200)
        self.send_header('content-type', 'text')

def main():
    PORT = 8000
    server = HTTPServer(('', PORT), requestHandler)
    print("Server running on port: " + PORT)
    server.serve_forever()

