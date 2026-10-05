import json
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA = [
    {"student_id":"S001","gpa":3.7,"attendance":95,"score":92,"status":" Active "},
    {"student_id":"S002","gpa":2.9,"attendance":82,"score":76,"status":"ACTIVE"},
    {"student_id":"S003","gpa":4.2,"attendance":91,"score":88,"status":"active"},
    {"student_id":"S004","gpa":3.1,"attendance":68,"score":61,"status":"inactive"},
    {"student_id":"S004","gpa":3.1,"attendance":68,"score":61,"status":"inactive"},
]

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/students":
            self.send_response(404); self.end_headers(); return
        body = json.dumps(DATA).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body)
    def log_message(self, *args):
        return

def create_server(host="127.0.0.1", port=8765):
    return HTTPServer((host, port), Handler)

if __name__ == "__main__":
    create_server().serve_forever()
