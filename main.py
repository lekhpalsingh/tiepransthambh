import cv2
import os
import time
from datetime import datetime

from ultralytics import YOLO
from firebase_client import upload_detection


# =========================================================
# PRANSTHAMBH - AI CAMERA + FIREBASE
# =========================================================

MODEL_PATH = "best.pt"

CAMERA_INDEX = 0

CONFIDENCE_THRESHOLD = 0.50

POLE_ID = "POLE_001"

ALERT_COOLDOWN = 30

ALERTS_FOLDER = "alerts"

os.makedirs(ALERTS_FOLDER, exist_ok=True)


# =========================================================
# LOAD AI MODEL
# =========================================================

print("=" * 60)
print("        PRANSTHAMBH")
print("AI WILDLIFE & ACCIDENT DETECTION")
print("=" * 60)

print()
print("Loading AI model...")

model = YOLO(MODEL_PATH)

print("Model loaded successfully!")
print("Classes:", model.names)


# =========================================================
# START CAMERA
# =========================================================

camera = cv2.VideoCapture(CAMERA_INDEX)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not camera.isOpened():

    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully.")
print("AI detection started.")
print()
print("Press Q to stop.")
print()


# =========================================================
# ALERT CONTROL
# =========================================================

last_alert_time = 0


# =========================================================
# MAIN LOOP
# =========================================================

try:

    while True:

        ret, frame = camera.read()

        if not ret:

            print("Camera frame error.")
            continue


        # -------------------------------------------------
        # AI DETECTION
        # -------------------------------------------------

        results = model(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )


        detections = []


        # -------------------------------------------------
        # READ DETECTIONS
        # -------------------------------------------------

        for result in results:

            if result.boxes is None:
                continue


            for box in result.boxes:

                class_id = int(box.cls[0])

                confidence = float(box.conf[0])

                class_name = model.names[class_id]


                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )


                detections.append({

                    "class_name": class_name,

                    "confidence": confidence,

                    "bbox": [x1, y1, x2, y2]

                })


        # -------------------------------------------------
        # DRAW DETECTIONS
        # -------------------------------------------------

        annotated_frame = frame.copy()


        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            class_name = detection["class_name"]

            confidence = detection["confidence"]


            label = (
                f"{class_name} "
                f"{confidence * 100:.1f}%"
            )


            # Bounding box

            cv2.rectangle(

                annotated_frame,

                (x1, y1),

                (x2, y2),

                (0, 0, 255),

                2

            )


            # Label background

            cv2.rectangle(

                annotated_frame,

                (x1, max(0, y1 - 30)),

                (
                    x1 + len(label) * 11 + 10,
                    y1
                ),

                (0, 0, 255),

                -1

            )


            # Label text

            cv2.putText(

                annotated_frame,

                label,

                (x1 + 5, y1 - 8),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                (255, 255, 255),

                2

            )


        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        if len(detections) == 0:

            status_text = "STATUS: NORMAL"

            status_color = (0, 255, 0)

        else:

            status_text = "STATUS: DETECTION"

            status_color = (0, 0, 255)


        cv2.putText(

            annotated_frame,

            status_text,

            (20, 35),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            status_color,

            2

        )


        # Pole ID

        cv2.putText(

            annotated_frame,

            f"POLE: {POLE_ID}",

            (20, 70),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 255),

            2

        )


        # PRANSTHAMBH

        cv2.putText(

            annotated_frame,

            "PRANSTHAMBH AI LIVE",

            (20, 105),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.6,

            (255, 255, 255),

            2

        )


        # -------------------------------------------------
        # SEND DETECTION TO FIREBASE
        # -------------------------------------------------

        current_time = time.time()


        if (

            len(detections) > 0

            and

            current_time - last_alert_time >= ALERT_COOLDOWN

        ):


            # Highest confidence detection

            best_detection = max(

                detections,

                key=lambda x: x["confidence"]

            )


            class_name = best_detection["class_name"]

            confidence = best_detection["confidence"]


            print()
            print("=" * 50)

            print("DETECTION FOUND!")

            print(
                f"Animal/Object : {class_name}"
            )

            print(
                f"Confidence    : "
                f"{confidence * 100:.2f}%"
            )

            print(
                f"Pole ID       : {POLE_ID}"
            )


            # -------------------------------------------------
            # SAVE ANNOTATED IMAGE
            # -------------------------------------------------

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )


            image_filename = (
                f"alert_{timestamp}.jpg"
            )


            image_path = os.path.join(

                ALERTS_FOLDER,

                image_filename

            )


            cv2.imwrite(

                image_path,

                annotated_frame

            )


            print(
                f"Image saved: {image_path}"
            )


            # -------------------------------------------------
            # FIREBASE UPLOAD
            # -------------------------------------------------

            firebase_result = upload_detection(

                class_name=class_name,

                confidence=confidence,

                pole_id=POLE_ID,

                image_path=image_path

            )


            if firebase_result:

                print(
                    "✅ FIREBASE: DATA SENT SUCCESSFULLY"
                )

            else:

                print(
                    "❌ FIREBASE: DATA SEND FAILED"
                )


            print("=" * 50)


            # Start cooldown

            last_alert_time = current_time


        # -------------------------------------------------
        # SHOW CAMERA
        # -------------------------------------------------

        cv2.imshow(

            "PRANSTHAMBH - AI CAMERA",

            annotated_frame

        )


        # -------------------------------------------------
        # PRESS Q TO EXIT
        # -------------------------------------------------

        key = cv2.waitKey(1) & 0xFF


        if key == ord("q"):

            break


# =========================================================
# STOP SAFELY
# =========================================================

except KeyboardInterrupt:

    print()
    print("System stopped by user.")


finally:

    camera.release()

    cv2.destroyAllWindows()

    print()
    print("PRANSTHAMBH stopped safely.")