from flask import Flask, render_template
import discord

app = Flask(__name__)

bot_stats = {
    "servers": 120,
    "users": 15320,
    "ping": "32ms"
}

@app.route("/")
def home():
    return render_template("index.html", stats=bot_stats)

@app.route("/invite")
def invite():
    return render_template("invite.html")

if __name__ == "__main__":
    app.run(port=3000)