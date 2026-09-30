import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import os

FIREBASE_KEY = "firebase-key.json"

# Firebase Realtime Database URL
FIREBASE_DATABASE_URL = "YOUR_FIREBASE_DATABASE_URL"

_firebase_initialized = False


def initialize_firebase():

    global _firebase_initialized

    if _firebase_initialized:
        return True

    try:

        if not os.path.exists(FIREBASE_KEY):
            print("Firebase key not found")
            return False

        cred = credentials.Certificate(FIREBASE_KEY)

        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": FIREBASE_DATABASE_URL
            }
        )

        _firebase_initialized = True

        print("Firebase connected successfully")

        return True

    except Exception as e:

        print("Firebase connection failed:", e)

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

        data = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "timestamp": now.isoformat(),

            "pole_id": pole_id,

            "detection": class_name,

            "confidence": round(confidence, 3),

            "status": (
                "ACCIDENT"
                if class_name == "Accident"
                else "WILDLIFE DETECTED"
            ),

            "image": image_path if image_path else ""
        }

        ref = db.reference("PRANSTHAMBH/Events")

        new_event = ref.push(data)

        print(
            "Firebase uploaded:",
            new_event.key
        )

        return True

    except Exception as e:

        print("Firebase upload failed:", e)

        return False