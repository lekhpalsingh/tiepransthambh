import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

FIREBASE_KEY = "firebase-key.json"

# IMPORTANT:
# Yahan apna actual Firebase Realtime Database URL paste karo.
FIREBASE_DATABASE_URL = "https://pransthambh-ai-default-rtdb.firebaseio.com/"

firebase_initialized = False


def initialize_firebase():

    global firebase_initialized

    if firebase_initialized:
        return True

    try:

        if not os.path.exists(FIREBASE_KEY):
            print("ERROR: firebase-key.json not found")
            return False

        cred = credentials.Certificate(FIREBASE_KEY)

        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": FIREBASE_DATABASE_URL
            }
        )

        firebase_initialized = True

        print("Firebase connected successfully!")

        return True

    except Exception as e:

        print("Firebase connection failed:")
        print(e)

        return False


def upload_detection(
    class_name,
    confidence,
    pole_id,
    image_path=None
):

    if not initialize_firebase():
        return False

    try:

        now = datetime.now()

        event_data = {

            "date": now.strftime("%Y-%m-%d"),

            "time": now.strftime("%H:%M:%S"),

            "timestamp": now.isoformat(),

            "pole_id": pole_id,

            "detection_class": class_name,

            "confidence": round(confidence, 4),

            "confidence_percent": round(
                confidence * 100,
                2
            ),

            "status":
                "ACCIDENT_DETECTED"
                if class_name == "Accident"
                else "WILDLIFE_DETECTED",

            "image_path":
                image_path if image_path else ""

        }

        ref = db.reference("PRANSTHAMBH/Events")

        new_event = ref.push(event_data)

        print(
            "Firebase event uploaded:",
            new_event.key
        )

        return True

    except Exception as e:

        print("Firebase upload failed:")
        print(e)

        return False