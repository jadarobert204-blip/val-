from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>💖 Question 💖</title>

<style>
body {
    margin: 0;
    overflow: hidden;
    font-family: Comic Sans MS, cursive;
    background: radial-gradient(circle, #ff69b4, #ffc0cb, #ffe4e1);
    text-align: center;
}

h1 {
    margin-top: 40px;
    font-size: 60px;
    color: white;
    text-shadow: 0 0 20px hotpink;
}

/* BUTTONS */
button {
    font-size: 60px;
    padding: 80px 140px;
    border-radius: 40px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

#yes {
    background: hotpink;
    color: white;
    box-shadow: 0 0 40px pink;
}

#no {
    background: #444;
    color: white;
    position: absolute;
}

/* FLOWERS */
.flower {
    position: absolute;
    font-size: 35px;
    opacity: 0.9;
    filter: drop-shadow(0 0 10px gold);
    animation: drift linear infinite;
}

@keyframes drift {
    0% { transform: translate(0,0) rotate(0deg); }
    100% { transform: translate(var(--x), var(--y)) rotate(360deg); }
}

/* CONFETTI */
.confetti {
    position: absolute;
    width: 12px;
    height: 12px;
    animation: fall 3s linear forwards;
}

@keyframes fall {
    to {
        transform: translateY(100vh) rotate(720deg);
        opacity: 0;
    }
}
</style>
</head>

<body>

<h1>💐 Would you be my girlfriend? 💐</h1>

<button id="yes" onclick="yesClick()">YES 💕</button>
<button id="no" onclick="noClick()">NO 🙅</button>

<!-- SOUNDS -->
<audio id="yesSound" src="https://actions.google.com/sounds/v1/crowds/large_crowd_cheer.ogg"></audio>
<audio id="noSound" src="https://actions.google.com/sounds/v1/human_voices/child_disappointed_mm.ogg"></audio>

<script>
let noScale = 1;
const noBtn = document.getElementById("no");
noBtn.style.top = "500px";
noBtn.style.left = "60%";

function noClick() {
    document.getElementById("noSound").play();

    let x = Math.random() * (window.innerWidth - 200);
    let y = Math.random() * (window.innerHeight - 200);

    noScale -= 0.12;
    noBtn.style.transform = `scale(${noScale})`;
    noBtn.style.left = x + "px";
    noBtn.style.top = y + "px";

    if (noScale <= 0.1) {
        noBtn.style.display = "none";
    }
}

function yesClick() {
    document.getElementById("yesSound").play();
    launchConfetti();
    alert("💖 YAAAAAAAY!!! 💖");
}

// CONFETTI
function launchConfetti() {
    for (let i = 0; i < 300; i++) {
        const c = document.createElement("div");
        c.className = "confetti";
        c.style.background = `hsl(${Math.random()*360},100%,50%)`;
        c.style.left = Math.random()*window.innerWidth + "px";
        c.style.top = "-10px";
        document.body.appendChild(c);
        setTimeout(()=>c.remove(),3000);
    }
}

// MANY FLOWERS (10x)
const flowers = ["🌸","🌺","🌼","🌻","💐","🌷"];
setInterval(() => {
    for (let i = 0; i < 10; i++) {
        const f = document.createElement("div");
        f.className = "flower";
        f.innerText = flowers[Math.floor(Math.random()*flowers.length)];
        f.style.left = Math.random()*window.innerWidth + "px";
        f.style.top = Math.random()*window.innerHeight + "px";
        f.style.setProperty("--x", (Math.random()*400-200)+"px");
        f.style.setProperty("--y", (Math.random()*400-200)+"px");
        f.style.animationDuration = (6+Math.random()*6)+"s";
        document.body.appendChild(f);
        setTimeout(()=>f.remove(),12000);
    }
}, 600);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run()