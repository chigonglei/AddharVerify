from http.server import BaseHTTPRequestHandler
import json
import re
from urllib.parse import urlparse, parse_qs

def is_valid_aadhaar(aadhaar):
    pattern = r"^[2-9]{1}[0-9]{11}$"
    return bool(re.match(pattern, aadhaar))

class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        query = parse_qs(urlparse(self.path).query)

        aadhaar = query.get("aadhaar", [""])[0]

        result = {
            "aadhaar": aadhaar,
            "valid": is_valid_aadhaar(aadhaar)
        }

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(result).encode())