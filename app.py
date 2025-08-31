from flask import Flask, request, jsonify, render_template_string
import joblib

app = Flask(__name__)

# Load model, encoders, and snack comments
model = joblib.load("snack_model.pkl")
le_mood = joblib.load("le_mood.pkl")
le_time = joblib.load("le_time.pkl")
le_snack = joblib.load("le_snack.pkl")
snack_comments = joblib.load("snack_comment.pkl")  # dictionary: snack -> comment

HTML_FORM = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Snack Recommender</title>
<style>
    body {
        margin: 0; padding: 0; height: 100vh;
        background: #000;
        font-family: 'Courier New', monospace;
        color: #0ff;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        overflow: hidden;
        cursor: crosshair;
    }
    h1 {
        font-size: 3em;
        font-weight: bold;
        color: #0ff;
        text-shadow: 0 0 3px #0ff33;
        z-index: 1; position: relative;
    }
    .option-btn {
        padding: 10px 18px;
        margin: 4px;
        border: none;
        border-radius: 12px;
        background: linear-gradient(135deg,#0ff,#f0f);
        color:#111;
        cursor:pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        z-index:1; position: relative;
    }
    .option-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 0 8px #0ff,0 0 15px #f0f;
    }
    .option-btn.active {
        background: linear-gradient(135deg,#ff0,#f0f);
        color:#000;
    }
    button#getSnackBtn {
        padding: 12px; margin: 8px; border-radius: 10px;
        border: none; font-size: 16px; z-index: 1; position: relative;
        background: linear-gradient(135deg, #0ff, #f0f);
        color: #111; cursor: pointer; transition: 0.3s;
    }
    button#getSnackBtn:hover { transform: scale(1.05); }
    #result {
        margin-top: 20px; font-size: 1.5em; color: #ff0;
        z-index: 1; position: relative; text-align: center;
    }
    .particle {
        position: absolute;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        pointer-events: none;
        opacity: 0.6;
        z-index: 0;
    }
</style>
</head>
<body>
<h1>Snack Recommender</h1>

<div id="mood-buttons">
  <button class="option-btn" data-value="happy">😊 Happy</button>
  <button class="option-btn" data-value="sad">😢 Sad</button>
  <button class="option-btn" data-value="angry">😡 Angry</button>
  <button class="option-btn" data-value="bored">😐 Bored</button>
  <button class="option-btn" data-value="excited">🤩 Excited</button>
  <button class="option-btn" data-value="stressed">😖 Stressed</button>
</div>

<div id="time-buttons">
  <button class="option-btn" data-value="morning">🌅 Morning</button>
  <button class="option-btn" data-value="afternoon">☀️ Afternoon</button>
  <button class="option-btn" data-value="evening">🌆 Evening</button>
  <button class="option-btn" data-value="night">🌙 Night</button>
  <button class="option-btn" data-value="midnight">🕛 Midnight</button>
</div>

<button id="getSnackBtn" onclick="getSnack()">Get Snack</button>
<div id="result"></div>

<script>
// Particle background
const colors = ["#0ff","#f0f","#ff0","#f00","#0f0","#f90"];
const particles = [];
for(let i=0;i<25;i++){
    const p = document.createElement('div');
    p.className='particle';
    p.style.background=colors[Math.floor(Math.random()*colors.length)];
    p.style.left=Math.random()*window.innerWidth+'px';
    p.style.top=Math.random()*window.innerHeight+'px';
    p.speedX=(Math.random()*2-1)*0.3;
    p.speedY=(Math.random()*2-1)*0.3;
    document.body.appendChild(p);
    particles.push(p);
}
function animateParticles(){
    particles.forEach(p=>{
        let x=parseFloat(p.style.left), y=parseFloat(p.style.top);
        x+=p.speedX; y+=p.speedY;
        if(x<0||x>window.innerWidth-15)p.speedX*=-1;
        if(y<0||y>window.innerHeight-15)p.speedY*=-1;
        p.style.left=x+'px'; p.style.top=y+'px';
    });
    requestAnimationFrame(animateParticles);
}
animateParticles();

// Button selection
let selectedMood="", selectedTime="";
document.querySelectorAll("#mood-buttons .option-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
        document.querySelectorAll("#mood-buttons .option-btn").forEach(b=>b.classList.remove("active"));
        btn.classList.add("active");
        selectedMood=btn.dataset.value;
    });
});
document.querySelectorAll("#time-buttons .option-btn").forEach(btn=>{
    btn.addEventListener("click",()=>{
        document.querySelectorAll("#time-buttons .option-btn").forEach(b=>b.classList.remove("active"));
        btn.classList.add("active");
        selectedTime=btn.dataset.value;
    });
});

// Snack API
async function getSnack(){
    if(!selectedMood || !selectedTime){ alert("Select both mood and time!"); return; }
    try{
        const response=await fetch("/recommend",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({mood:selectedMood,time:selectedTime})
        });
        const data=await response.json();
        if(data.error){
            document.getElementById('result').innerText="Error: "+data.error;
        } else {
            document.getElementById('result').innerHTML=`<b>${data.snack}</b> <br><i>${data.comment}</i>`;
        }
    }catch(err){
        document.getElementById('result').innerText="Server error: "+err;
    }
}
</script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_FORM)

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    mood = data.get("mood")
    time = data.get("time")
    if not mood or not time:
        return jsonify({"error":"Missing mood or time"}),400
    try:
        mood_enc = le_mood.transform([mood])[0]
        time_enc = le_time.transform([time])[0]
        pred = model.predict([[mood_enc,time_enc]])[0]
        snack = le_snack.inverse_transform([pred])[0]
        comment = snack_comments.get(snack,"Enjoy it, or whatever... 😏")
        return jsonify({"snack":snack,"comment":comment})
    except Exception as e:
        return jsonify({"error":str(e)}),500

if __name__=="__main__":
    app.run(debug=True)
