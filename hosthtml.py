import http.server
import socketserver

# Define the port you want to host the HTML file on
PORT = 8000

# Define the request handler class
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    # Override the default behavior to set CORS headers
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

# Create a socket server with the specified port and request handler
with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
    print("Server started at localhost:" + str(PORT))

    # Serve the HTML file indefinitely
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
