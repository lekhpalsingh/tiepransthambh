import requests
import time
import os
from datetime import datetime

# ==========================================
# TELEGRAM CONFIG
# ==========================================

BOT_TOKEN = "YOUR_NEW_BOT_TOKEN"
CHAT_ID = "1473474086"

# ==========================================
# IMAGES
# ==========================================

images = [
    "alerts/image1.jpg",
    "alerts/image2.jpg",
    "alerts/image3.jpg",
    "alerts/image4.jpg",
    "alerts/image5.jpg"
]

# ==========================================
# SEND IMAGES ONE BY ONE
# ==========================================

for i, image_path in enumerate(images, start=1):

    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        continue

    now = datetime.now()

    date = now.strftime("%d-%m-%Y")
    current_time = now.strftime("%I:%M:%S %p")

    caption = f"""
🚨 PRANSTHAMBH ACCIDENT ALERT 🚨

📸 Evidence Image: {i}/{len(images)}

📅 Date: {date}
🕒 Time: {current_time}

⚠️ Detection: Accident
📍 Pole ID: POLE_001

🚑 Emergency response required.
"""

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"

    try:

        with open(image_path, "rb") as photo:

            response = requests.post(
                url,
                data={
                    "chat_id": CHAT_ID,
                    "caption": caption
                },
                files={
                    "photo": photo
                },
                timeout=30
            )

        if response.status_code == 200:
            print(f"✅ Image {i} sent successfully")
        else:
            print(f"❌ Image {i} failed")
            print(response.text)

    except Exception as e:
        print(f"❌ Error sending image {i}: {e}")

    # 10 second delay before next image
    if i < len(images):
        print("⏳ Waiting 10 seconds...")
        time.sleep(10)

print("\n✅ All Telegram images processed.")