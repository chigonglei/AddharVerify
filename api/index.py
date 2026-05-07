from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def is_valid_aadhaar(aadhaar):
    pattern = r"^[2-9]{1}[0-9]{11}$"
    return bool(re.match(pattern, aadhaar))

@app.route("/")
def home():

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Aadhaar Validator</title>

        <style>
            body{
                font-family:Arial;
                background:#0f172a;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                margin:0;
            }

            .card{
                background:white;
                padding:30px;
                border-radius:20px;
                width:350px;
                text-align:center;
            }

            input{
                width:100%;
                padding:14px;
                margin-top:10px;
                border:1px solid #ccc;
                border-radius:10px;
            }

            button{
                width:100%;
                padding:14px;
                margin-top:15px;
                border:none;
                background:#2563eb;
                color:white;
                border-radius:10px;
                cursor:pointer;
            }

            #result{
                margin-top:20px;
                font-size:18px;
                font-weight:bold;
            }
        </style>
    </head>

    <body>

        <div class="card">

            <h1>Aadhaar Validator</h1>

            <input type="text" id="aadhaar" placeholder="Enter Aadhaar Number">

            <button onclick="validateAadhaar()">
                Validate
            </button>

            <div id="result"></div>

        </div>

        <script>

            async function validateAadhaar(){

                const aadhaar = document.getElementById("aadhaar").value;

                const response = await fetch(`/api/validate?aadhaar=${aadhaar}`);

                const data = await response.json();

                const result = document.getElementById("result");

                if(data.valid){
                    result.innerHTML = "✅ Valid Aadhaar Number";
                    result.style.color = "green";
                }else{
                    result.innerHTML = "❌ Invalid Aadhaar Number";
                    result.style.color = "red";
                }
            }

        </script>

    </body>
    </html>
    """

@app.route("/api/validate")
def validate():

    aadhaar = request.args.get("aadhaar", "")

    return jsonify({
        "aadhaar": aadhaar,
        "valid": is_valid_aadhaar(aadhaar)
    })

app = app