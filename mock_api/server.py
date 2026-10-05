import json
from http.server import BaseHTTPRequestHandler, HTTPServer

DATA = [
    {"student_id": "S001", "gpa": 3.7, "attendance": 95, "score": 92, "status": " Active "},
    {"student_id": "S002", "gpa": 2.9, "attendance": 82, "score": 76, "status": "ACTIVE"},
    {"student_id": "S003", "gpa": 4.2, "attendance": 91, "score": 88, "status": "active"},
    {"student_id": "S004", "gpa": 3.1, "attendance": 68, "score": 61, "status": "inactive"},
    {"student_id": "S004", "gpa": 3.1, "attendance": 68, "score": 61, "status": "inactive"},
]

WEB_DATA = [
    {"student_id": "S001", "student_name": "Ali", "age": 22, "major": "CS", "city": "Sanaa"},
    {"student_id": "S002", "student_name": "Ahmed", "age": 21, "major": "IS", "city": "sanaa"},
    {"student_id": "S003", "student_name": "Sara", "age": 23, "major": "CS", "city": "Hodeidah"},
    {"student_id": "S004", "student_name": "Omar", "age": 20, "major": "IT", "city": "Dhamar"},
    {"student_id": "S005", "student_name": "Mona", "age": 22, "major": "CS", "city": "Ibb"},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/students":
            body = json.dumps(DATA).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/web-students":
            rows = "".join(
                f"""
                <tr>
                    <td>{r['student_id']}</td>
                    <td>{r['student_name']}</td>
                    <td>{r['age']}</td>
                    <td>{r['major']}</td>
                    <td>{r['city']}</td>
                </tr>
                """
                for r in WEB_DATA
            )

            html = f"""
            <html>
            <body>
                <table id="students">
                    <thead>
                        <tr>
                            <th>student_id</th>
                            <th>student_name</th>
                            <th>age</th>
                            <th>major</th>
                            <th>city</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </body>
            </html>
            """

            body = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, *args):
        return


def create_server(host="127.0.0.1", port=8765):
    return HTTPServer((host, port), Handler)


if __name__ == "__main__":
    create_server().serve_forever()