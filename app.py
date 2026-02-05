from flask import Flask, render_template_string, request
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# ---------- Email Function ----------
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")  # your Gmail
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")  # Gmail App Password
TO_EMAIL = os.environ.get("TO_EMAIL", EMAIL_ADDRESS)

def send_email(answer):
    msg = MIMEMultipart()
    msg['From'] = triumphfrancis206@gmail.com
    msg['To'] = triumphfrancis206@gmail.com
    msg['Subject'] = f"💖 Girlfriend Game Response: {answer}"

    body = f"🌸 The user clicked: {answer}\nTime: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"Email sent: {answer}")
    except Exception as e:
        print("Failed to send email:", e)

# ---------- HTML Game ----------
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>💖 Will you be my girlfriend? 💖</title>
<style>
body { margin:0; overflow:hidden; font-family: Comic Sans MS, cursive;
       background: radial-gradient(circle, #ff69b4, #ffc0cb, #ffe4e1); text-align:center;}
h1 { margin-top:40px; font-size:60px; color:white; text-shadow:0 0 20px hotpink;}
button { font-size:60px; padding:80px 140px; border-radius:40px; border:none; cursor:pointer; transition: all 0.3s ease; z-index:10; position: relative;}
#yes { background: hotpink; color:white; box-shadow:0 0 40px pink;}
#no { background:#444; color:white; position:absolute; z-index:10;}
#startOverlay { position: fixed; top:0; left:0; width:100%; height:100%; background:#ffb6c1; display:flex; align-items:center; justify-content:center; z-index:9999; cursor:pointer;}
#startOverlay h1 { font-size:50px; color:white; text-shadow:2px 2px 10px hotpink; }
#gameCanvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; }
</style>
</head>
<body>

<div id="startOverlay"><h1>💖 Tap to Start 💖</h1></div>

<h1>💐 Will you be my girlfriend? 💐</h1>
<button id="yes">YES 💕</button>
<button id="no">NO 🙅</button>

<!-- Audio -->
<audio id="bgMusic" loop>
  <source src="https://actions.google.com/sounds/v1/ambiences/romantic_piano.ogg" type="audio/ogg">
</audio>
<audio id="yesSound" preload="auto">
  <source src="https://actions.google.com/sounds/v1/crowds/large_crowd_cheer.ogg" type="audio/ogg">
</audio>
<audio id="noSound" preload="auto">
  <source src="https://actions.google.com/sounds/v1/human_voices/child_disappointed_mm.ogg" type="audio/ogg">
</audio>

<canvas id="gameCanvas"></canvas>

<script>
// ---------- SETUP ----------
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth; canvas.height = window.innerHeight;

let audioUnlocked = false;
const bgMusic = document.getElementById("bgMusic");
const yesSound = document.getElementById("yesSound");
const noSound = document.getElementById("noSound");
const overlay = document.getElementById("startOverlay");

overlay.addEventListener("click", unlockAudio);
overlay.addEventListener("touchend", unlockAudio);

function unlockAudio() {
    if(audioUnlocked) return;
    try { bgMusic.muted=false; bgMusic.play(); } catch(e){console.log("Audio blocked");}
    overlay.style.display="none"; audioUnlocked=true;
}

// ---------- FLOWERS ----------
class Flower {
    constructor() {
        this.x=Math.random()*canvas.width; this.y=Math.random()*canvas.height;
        this.size=25+Math.random()*20;
        this.speedX=(Math.random()-0.5)*1.5; this.speedY=(Math.random()-0.5)*1.5;
        const emojis=["🌸","🌺","🌼","🌻","💐","🌷"];
        this.char=emojis[Math.floor(Math.random()*emojis.length)];
    }
    draw(){ ctx.font=this.size+"px serif"; ctx.fillText(this.char,this.x,this.y); }
    update(){ this.x+=this.speedX; this.y+=this.speedY;
        if(this.x<0) this.x=canvas.width; if(this.x>canvas.width) this.x=0;
        if(this.y<0) this.y=canvas.height; if(this.y>canvas.height) this.y=0;
    }
}
const flowers=[]; for(let i=0;i<100;i++) flowers.push(new Flower());

// ---------- CONFETTI ----------
class Confetti {
    constructor(){ this.x=Math.random()*canvas.width; this.y=-10; this.size=8+Math.random()*8;
        this.color=`hsl(${Math.random()*360},100%,50%)`; this.speedY=2+Math.random()*3;
        this.angle=Math.random()*360; this.spin=0.1+Math.random()*0.3;
    }
    draw(){ ctx.save(); ctx.translate(this.x,this.y); ctx.rotate(this.angle); ctx.fillStyle=this.color; ctx.fillRect(-this.size/2,-this.size/2,this.size,this.size); ctx.restore(); }
    update(){ this.y+=this.speedY; this.angle+=this.spin; }
}
let confettis=[];

// ---------- ANIMATION LOOP ----------
function animate(){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    flowers.forEach(f=>{ f.update(); f.draw(); });
    confettis.forEach((c,i)=>{ c.update(); c.draw(); if(c.y>canvas.height) confettis.splice(i,1); });
    requestAnimationFrame(animate);
}
animate();

// ---------- YES / NO BUTTON ----------
let noBtn = document.getElementById("no"); let noScale=1;
noBtn.style.top="500px"; noBtn.style.left="60%";

function sendResponse(answer){
    fetch(`/response?answer=${answer}`).catch(e=>console.log(e));
}

function moveNoButtonAway(e){
    if(!audioUnlocked || noScale<=0.1) return;
    let rect=noBtn.getBoundingClientRect();
    let mouseX=e.clientX || e.touches[0].clientX;
    let mouseY=e.clientY || e.touches[0].clientY;
    let dx=rect.left+rect.width/2 - mouseX;
    let dy=rect.top+rect.height/2 - mouseY;
    let dist=Math.sqrt(dx*dx + dy*dy);
    if(dist<150){
        let angle=Math.atan2(dy,dx);
        let moveX=Math.cos(angle)*120;
        let moveY=Math.sin(angle)*120;
        let newX=Math.min(Math.max(0,rect.left+moveX),window.innerWidth-rect.width);
        let newY=Math.min(Math.max(0,rect.top+moveY),window.innerHeight-rect.height);
        noBtn.style.left=newX+"px";
        noBtn.style.top=newY+"px";
        noScale-=0.08; noBtn.style.transform=`scale(${noScale})`;
        if(noScale<=0.1) noBtn.style.display="none";
        noSound.play();
        sendResponse("NO");
    }
}
document.addEventListener("mousemove", moveNoButtonAway);
document.addEventListener("touchmove", moveNoButtonAway,{passive:true});

document.getElementById("yes").addEventListener("click", ()=>{
    if(!audioUnlocked) return;
    yesSound.play();
    for(let i=0;i<200;i++) confettis.push(new Confetti());
    sendResponse("YES");
    alert("💖 YAAAAAAAY!!! 💖");
});

// ---------- RESIZE ----------
window.addEventListener("resize", ()=>{ canvas.width=window.innerWidth; canvas.height=window.innerHeight; });
</script>
</body>
</html>
"""

# ---------- FLASK ROUTES ----------
@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/response")
def response():
    answer = request.args.get("answer", "unknown")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Save locally
    with open("responses.txt","a") as f:
        f.write(f"{timestamp}: {answer}\n")
    print(f"Response logged: {answer}")
    
    # Send email notification
    send_email(answer)
    return "OK"

if __name__ == "__main__":
    app.run()
