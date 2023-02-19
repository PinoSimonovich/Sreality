
import http.server
import socketserver

hostName = "localhost"
serverPort = 8080

class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

handler = HttpRequestHandler

with socketserver.TCPServer(("0.0.0.0", serverPort), handler) as httpd:
    print("Http Server Serving at localhost port", serverPort)
    httpd.serve_forever()
