from flask import Flask, request, jsonify
import re
import time

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

            *{
                margin:0;
                padding:0;
                box-sizing:border-box;
            }

            body{
                font-family:Arial;
                background:#0f172a;
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                padding:20px;
            }

            .card{
                width:100%;
                max-width:400px;
                background:white;
                padding:30px;
                border-radius:20px;
                text-align:center;
                box-shadow:0 10px 30px rgba(0,0,0,0.3);
            }

            h1{
                margin-bottom:25px;
                color:#0f172a;
            }

            input{
                width:100%;
                padding:15px;
                border:1px solid #ddd;
                border-radius:12px;
                font-size:16px;
            }

            button{
                width:100%;
                margin-top:15px;
                padding:15px;
                border:none;
                border-radius:12px;
                background:#2563eb;
                color:white;
                font-size:16px;
                cursor:pointer;
            }

            button:hover{
                background:#1d4ed8;
            }

            #result{
                margin-top:25px;
                font-size:18px;
                font-weight:bold;
            }

            .loading{
                color:#2563eb;
            }

            .valid{
                color:green;
            }

            .invalid{
                color:red;
            }

            .info{
                color:#555;
                margin-top:10px;
                font-size:14px;
            }

        </style>

    </head>

    <body>

        <div class="card">

            <h1>Aadhaar Validator</h1>

            <input 
                type="text" 
                id="aadhaar" 
                maxlength="12"
                placeholder="Enter 12-digit Aadhaar"
                oninput="resetResult()"
            >

            <button onclick="validateAadhaar()">
                Check Aadhaar
            </button>

            <div id="result"></div>

            <div class="info" id="info">
                Ready for verification
            </div>

        </div>

        <script>

            function resetResult(){

                document.getElementById("result").innerHTML = "";

                document.getElementById("info").innerHTML =
                    "Enter another Aadhaar number to check";
            }

            async function validateAadhaar(){

                const aadhaar =
                    document.getElementById("aadhaar").value.trim();

                const result =
                    document.getElementById("result");

                const info =
                    document.getElementById("info");

                if(aadhaar.length !== 12){

                    result.innerHTML =
                        "❌ Aadhaar must contain exactly 12 digits";

                    result.className = "invalid";

                    info.innerHTML =
                        "Please enter a valid 12-digit number";

                    return;
                }

                result.innerHTML = "⏳ Checking...";

                result.className = "loading";

                info.innerHTML = "Verifying Aadhaar number";

                const response =
                    await fetch(`/api/validate?aadhaar=${aadhaar}`);

                const data = await response.json();

                if(data.valid){

                    result.innerHTML =
                        "✅ Valid Aadhaar Number";

                    result.className = "valid";

                    info.innerHTML =
                        "Verification completed successfully";

                }else{

                    result.innerHTML =
                        "❌ Invalid Aadhaar Number";

                    result.className = "invalid";

                    info.innerHTML =
                        "Entered Aadhaar is not valid";
                }
            }

        </script>

    </body>
    </html>
    """


@app.route("/api/validate")
def validate():

    aadhaar = request.args.get("aadhaar", "").strip()

    time.sleep(1.5)

    return jsonify({
        "aadhaar": aadhaar,
        "valid": is_valid_aadhaar(aadhaar)
    })

app = app