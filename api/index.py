from flask import Flask, request, jsonify
import re
import time

app = Flask(__name__)

def is_valid_aadhaar(aadhaar):

    if not re.match(r"^[2-9][0-9]{11}$", aadhaar):
        return False

    d = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,2,3,4,0,6,7,8,9,5],
        [2,3,4,0,1,7,8,9,5,6],
        [3,4,0,1,2,8,9,5,6,7],
        [4,0,1,2,3,9,5,6,7,8],
        [5,9,8,7,6,0,4,3,2,1],
        [6,5,9,8,7,1,0,4,3,2],
        [7,6,5,9,8,2,1,0,4,3],
        [8,7,6,5,9,3,2,1,0,4],
        [9,8,7,6,5,4,3,2,1,0]
    ]

    p = [
        [0,1,2,3,4,5,6,7,8,9],
        [1,5,7,6,2,8,3,0,9,4],
        [5,8,0,3,7,9,6,1,4,2],
        [8,9,1,6,0,4,3,5,2,7],
        [9,4,5,3,1,2,6,8,7,0],
        [4,2,8,6,5,7,3,9,0,1],
        [2,7,9,3,8,0,6,4,1,5],
        [7,0,4,6,9,1,3,2,5,8]
    ]

    c = 0

    reversed_digits = list(map(int, reversed(aadhaar)))

    for i, item in enumerate(reversed_digits):
        c = d[c][p[i % 8][item]]

    return c == 0


@app.route("/")
def home():

    return """
    <!DOCTYPE html>
<html>
<head>

<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>Aadhaar Validator</title>

<style>

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

body{
    font-family:Arial,sans-serif;
    background:#020b24;
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    padding:20px;
    color:white;
}

.container{
    width:100%;
    max-width:420px;
}

.logo{
    text-align:center;
    margin-bottom:30px;
}

.logo h1{
    font-size:48px;
    font-weight:800;
    line-height:1.1;
}

.logo span{
    color:#2f7cff;
}

.logo p{
    margin-top:15px;
    color:#b8c1d1;
    font-size:16px;
}

.card{
    background:rgba(255,255,255,0.05);
    border:1px solid rgba(255,255,255,0.08);
    border-radius:25px;
    padding:25px;
    backdrop-filter:blur(10px);
}

.label{
    margin-bottom:15px;
    font-size:15px;
    color:#d1d5db;
}

.input-box{
    background:white;
    border-radius:18px;
    overflow:hidden;
}

input{
    width:100%;
    border:none;
    outline:none;
    padding:18px;
    font-size:22px;
    text-align:center;
}

button{
    width:100%;
    margin-top:20px;
    border:none;
    border-radius:18px;
    padding:18px;
    background:linear-gradient(90deg,#2563eb,#3b82f6);
    color:white;
    font-size:20px;
    font-weight:bold;
    cursor:pointer;
}

button:hover{
    opacity:0.9;
}

.result-card{
    margin-top:25px;
    border-radius:25px;
    padding:25px;
    text-align:center;
    display:none;
}

.valid{
    background:rgba(34,197,94,0.12);
    border:1px solid rgba(34,197,94,0.4);
}

.invalid{
    background:rgba(239,68,68,0.12);
    border:1px solid rgba(239,68,68,0.4);
}

.loading{
    background:rgba(59,130,246,0.12);
    border:1px solid rgba(59,130,246,0.4);
}

.status{
    font-size:30px;
    margin-bottom:15px;
}

.message{
    font-size:26px;
    font-weight:bold;
}

.sub{
    margin-top:12px;
    color:#d1d5db;
    line-height:1.6;
    font-size:16px;
}

.footer{
    margin-top:30px;
    text-align:center;
    color:#94a3b8;
    font-size:15px;
}

.footer span{
    color:#60a5fa;
    font-weight:bold;
}

@media(max-width:480px){

    .logo h1{
        font-size:42px;
    }

    input{
        font-size:20px;
    }

    .message{
        font-size:22px;
    }
}

</style>

</head>

<body>

<div class="container">

    <div class="logo">

        <h1>
            Aadhaar <br>
            <span>Validator</span>
        </h1>

        <p>
            Validate your 12-digit Aadhaar Number
        </p>

    </div>

    <div class="card">

        <div class="label">
            Enter 12-digit Aadhaar Number
        </div>

        <div class="input-box">

            <input
                type="text"
                id="aadhaar"
                maxlength="12"
                placeholder="741694613161"
                oninput="resetResult()"
            >

        </div>

        <button onclick="validateAadhaar()">
            🔍 Check Aadhaar
        </button>

    </div>

    <div id="resultCard" class="result-card">

        <div id="status" class="status"></div>

        <div id="message" class="message"></div>

        <div id="sub" class="sub"></div>

    </div>

    <div class="footer">
        Made with ❤️ by <span>Sanjoy-Khoirom (Vercel)</span>
    </div>

</div>

<script>

function resetResult(){

    document.getElementById("resultCard").style.display = "none";
}

async function validateAadhaar(){

    const aadhaar =
        document.getElementById("aadhaar").value.trim();

    const card =
        document.getElementById("resultCard");

    const status =
        document.getElementById("status");

    const message =
        document.getElementById("message");

    const sub =
        document.getElementById("sub");

    card.style.display = "block";

    if(aadhaar.length !== 12){

        card.className = "result-card invalid";

        status.innerHTML = "❌";

        message.innerHTML = "Invalid Aadhaar";

        sub.innerHTML =
            "Aadhaar must contain exactly 12 digits";

        return;
    }

    card.className = "result-card loading";

    status.innerHTML = "⏳";

    message.innerHTML = "Checking Aadhaar";

    sub.innerHTML =
        "Please wait while verification completes";

    const response =
        await fetch(`/api/validate?aadhaar=${aadhaar}`);

    const data = await response.json();

    if(data.valid){

        card.className = "result-card valid";

        status.innerHTML = "✅";

        message.innerHTML = "Valid Aadhaar Number";

        sub.innerHTML =
            `Verification completed successfully for Aadhaar ${aadhaar}`;

    }else{

        card.className = "result-card invalid";

        status.innerHTML = "❌";

        message.innerHTML = "Invalid Aadhaar Number";

        sub.innerHTML =
            `Verification failed for Aadhaar ${aadhaar}`;
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