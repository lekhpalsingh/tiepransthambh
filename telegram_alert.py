import requests
import os

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_alert(
    class_name,
    confidence,
    pole_id,
    image_path=None
):

    try:

        message = (
            "🚨 PRANSTHAMBH ALERT 🚨\n\n"
            f"Detection: {class_name}\n"
            f"Confidence: {confidence:.2f}\n"
            f"Pole ID: {pole_id}\n"
        )

        if class_name == "Accident":

            message += (
                "\n⚠️ ACCIDENT DETECTED\n"
                "Emergency response required."
            )

        else:

            message += (
                "\n🦌 Wildlife detected."
            )

        url = (
            f"https://api.telegram.org/"
            f"bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        )

        response = requests.post(
            url,
            data={
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message
            },
            timeout=10
        )

        if response.status_code != 200:

            print(
                "Telegram message failed:",
                response.text
            )

            return False

        # Send image if available
        if image_path and os.path.exists(image_path):

            photo_url = (
                f"https://api.telegram.org/"
                f"bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            )

            with open(image_path, "rb") as photo:

                photo_response = requests.post(
                    photo_url,
                    data={
                        "chat_id": TELEGRAM_CHAT_ID
                    },
                    files={
                        "photo": photo
                    },
                    timeout=20
                )

            if photo_response.status_code != 200:

                print(
                    "Telegram photo failed:",
                    photo_response.text
                )

                return False

        print("TELEGRAM ALERT SENT!")

        return True

    except Exception as e:

        print(
            "Telegram connection failed:",
            e
        )

        return False