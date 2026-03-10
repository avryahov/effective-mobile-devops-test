import os
from http.server import BaseHTTPRequestHandler, HTTPServer


DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 8080
DEFAULT_RESPONSE = "Hello from Effective Mobile!"
HOST = os.getenv("APP_HOST", DEFAULT_HOST)
PORT = int(os.getenv("APP_PORT", str(DEFAULT_PORT)))
RESPONSE_FILE = os.getenv("APP_RESPONSE_FILE", "/run/secrets/backend_response.txt")


def load_response_body():
    if os.path.exists(RESPONSE_FILE):
        with open(RESPONSE_FILE, "r", encoding="utf-8") as secret_file:
            value = secret_file.read().strip()
            if value:
                return value.encode("utf-8")

    return os.getenv("APP_RESPONSE", DEFAULT_RESPONSE).encode("utf-8")


RESPONSE_BODY = load_response_body()


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/healthz":
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

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
