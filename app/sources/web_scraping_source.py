from html.parser import HTMLParser
from urllib.request import urlopen


class StudentTableParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headers = []
        self.rows = []
        self.current_row = []
        self.current_cell = ""
        self.in_header = False
        self.in_cell = False

    def handle_starttag(self, tag, attrs):
        if tag == "th":
            self.in_header = True
            self.current_cell = ""
        elif tag == "td":
            self.in_cell = True
            self.current_cell = ""
        elif tag == "tr":
            self.current_row = []

    def handle_data(self, data):
        if self.in_header or self.in_cell:
            self.current_cell += data

    def handle_endtag(self, tag):
        if tag == "th":
            self.headers.append(self.current_cell.strip())
            self.in_header = False
        elif tag == "td":
            self.current_row.append(self.current_cell.strip())
            self.in_cell = False
        elif tag == "tr" and self.current_row:
            self.rows.append(self.current_row)

    def result(self):
        return [
            dict(zip(self.headers, row))
            for row in self.rows
            if len(row) == len(self.headers)
        ]


def extract_web_students(url: str):
    with urlopen(url, timeout=5) as response:
        if response.status != 200:
            raise RuntimeError(f"Web page returned HTTP {response.status}")

        html = response.read().decode("utf-8")

    parser = StudentTableParser()
    parser.feed(html)
    return parser.result()