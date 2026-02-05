from flask import Flask, request, Response
import smtplib, os, datetime, threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL", EMAIL_ADDRESS)

def send_email_background(answer):
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print("Email env vars missing")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = "💖 Girlfriend Game Response"

        body = f"""
Someone responded 💌

Answer: {answer}
Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>💖 A Question</title>
<style>
body{margin:0;height:100vh;overflow:hidden;background:radial-gradient(circle,#ffb6c1,#ff69b4);font-family:Comic Sans MS,cursive}
.note{position:absolute;top:20px;width:100%;text-align:center;font-size:32px;color:white}
.center{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)}
button{font-size:40px;padding:40px 80px;border-radius:25px;border:none;cursor:pointer}
#yes{background:#00ff99}
#no{background:#ff4444;position:absolute}
.flower{position:absolute;animation:float 12s linear infinite;opacity:.85}
@keyframes float{from{transform:translateY(100vh)}to{transform:translateY(-120px)}}
</style>
</head>
<body>

<div class="note">🌸 Will you be my girlfriend? 🌸</div>

<div class="center">
<button id="yes">YES 💖</button>
</div>

<button id="no">NO 😤</button>

<audio id="yesSound" src="https://cdn.pixabay.com/download/audio/2022/03/15/audio_7c5c8f0c69.mp3"></audio>
<audio id="noSound" src="https://cdn.pixabay.com/download/audio/2022/10/03/audio_6c8f5b1f90.mp3"></audio>
<audio id="bgSound" src="https://cdn.pixabay.com/download/audio/2022/08/02/audio_7b3a4b7b44.mp3" loop></audio>

<script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
<script>
const noBtn=document.getElementById("no"),yesBtn=document.getElementById("yes");
document.body.addEventListener("click",()=>{bgSound.play()},{once:true});
let scale=1;

noBtn.onclick=()=>{
noSound.play();
scale-=.15;
noBtn.style.transform=`scale(${scale})`;
noBtn.style.left=Math.random()*80+"vw";
noBtn.style.top=Math.random()*80+"vh";
fetch("/response?answer=NO");
if(scale<=0)noBtn.remove();
};

yesBtn.onclick=()=>{
yesSound.play();
confetti({particleCount:200,spread:120});
fetch("/response?answer=YES");
};

for(let i=0;i<120;i++){
let f=document.createElement("div");
f.innerHTML="🌸";
f.className="flower";
f.style.left=Math.random()*100+"vw";
f.style.fontSize=20+Math.random()*30+"px";
f.style.animationDuration=6+Math.random()*10+"s";
document.body.appendChild(f);
}
</script>
</body>
</html>"""

@app.route("/")
def index():
    return Response(HTML, mimetype="text/html")

@app.route("/response")
def response():
    answer = request.args.get("answer")
    print("Response logged:", answer)

    threading.Thread(
        target=send_email_background,
        args=(answer,),
        daemon=True
    ).start()

    return ("", 204)

if __name__ == "__main__":
    app.run()
