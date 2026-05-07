async function checkAadhaar(){

    const aadhaar = document.getElementById("aadhaar").value;

    const result = document.getElementById("result");

    result.innerHTML = "Checking...";

    const response = await fetch(`/api/validate?aadhaar=${aadhaar}`);

    const data = await response.json();

    if(data.valid){
        result.innerHTML = "✅ Valid Aadhaar Number";
        result.style.color = "green";
    }else{
        result.innerHTML = "❌ Invalid Aadhaar Number";
        result.style.color = "red";
    }
}