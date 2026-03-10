from http.server import BaseHTTPRequestHandler, HTTPServer


HOST = "0.0.0.0"
PORT = 8080
RESPONSE_BODY = b"Hello from Effective Mobile!"


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not Found")
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(RESPONSE_BODY)))
        self.end_headers()
        self.wfile.write(RESPONSE_BODY)

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), RequestHandler)
    server.serve_forever()
