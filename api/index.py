from flask import Flask, request, jsonify, send_from_directory
import re
import os

app = Flask(__name__, static_folder="../public")

def is_valid_aadhaar(aadhaar):
    pattern = r"^[2-9]{1}[0-9]{11}$"
    return bool(re.match(pattern, aadhaar))

@app.route("/")
def home():
    return send_from_directory("../public", "index.html")

@app.route("/style.css")
def style():
    return send_from_directory("../public", "style.css")

@app.route("/app.js")
def js():
    return send_from_directory("../public", "app.js")

@app.route("/api/validate")
def validate():

    aadhaar = request.args.get("aadhaar", "")

    return jsonify({
        "aadhaar": aadhaar,
        "valid": is_valid_aadhaar(aadhaar)
    })

if __name__ == "__main__":
    app.run(debug=True)