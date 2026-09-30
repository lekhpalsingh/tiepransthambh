import cv2
import os
import time
from datetime import datetime

from camera import start_camera
from detection import PransthambhDetector
from alert_manager import AlertManager
from firebase_client import upload_detection
from telegram_alert import send_telegram_alert

from config import (
    POLE_ID,
    ALERTS_FOLDER,
    ACCIDENT_CLASS
)


# =========================================================
# PRANSTHAMBH MAIN SYSTEM
# =========================================================

def main():

    print("=" * 60)
    print("       PRANSTHAMBH")
    print("SMART WILDLIFE & ACCIDENT DETECTION SYSTEM")
    print("=" * 60)

    # Create folders
    os.makedirs(ALERTS_FOLDER, exist_ok=True)

    # Start camera
    camera = start_camera()

    # Load AI
    detector = PransthambhDetector()

    # GPIO alert manager
    alert_manager = AlertManager()

    # Last alert time
    last_alert_time = 0

    print()
    print("PRANSTHAMBH SYSTEM READY")
    print("AI detection started")
    print("Press Q to stop")
    print()

    try:

        while True:

            ret, frame = camera.read()

            if not ret:

                print("Camera frame error")
                continue

            # =================================================
            # AI DETECTION
            # =================================================

            detections = detector.detect(frame)

            # =================================================
            # DRAW BOX + CLASS + CONFIDENCE
            # =================================================

            annotated_frame = detector.draw_detections(
                frame,
                detections
            )

            # =================================================
            # NORMAL CONDITION
            # =================================================

            if len(detections) == 0:

                alert_manager.normal_state()

                cv2.putText(
                    annotated_frame,
                    "STATUS: NORMAL",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

            # =================================================
            # DETECTION CONDITION
            # =================================================

            else:

                alert_manager.alert_state()

                current_time = time.time()

                # Print detections
                for detection in detections:

                    class_name = detection["class_name"]
                    confidence = detection["confidence"]

                    print(
                        f"DETECTED: {class_name} | "
                        f"Confidence: "
                        f"{confidence * 100:.1f}% | "
                        f"Pole: {POLE_ID}"
                    )

                # =================================================
                # COOLDOWN
                # =================================================

                if current_time - last_alert_time >= 30:

                    # Use highest-confidence detection
                    best_detection = max(
                        detections,
                        key=lambda x: x["confidence"]
                    )

                    class_name = best_detection["class_name"]
                    confidence = best_detection["confidence"]

                    # =================================================
                    # SAVE ANNOTATED FRAME
                    # =================================================

                    timestamp = datetime.now().strftime(
                        "%Y%m%d_%H%M%S"
                    )

                    image_path = os.path.join(
                        ALERTS_FOLDER,
                        f"alert_{timestamp}.jpg"
                    )

                    cv2.imwrite(
                        image_path,
                        annotated_frame
                    )

                    print(
                        f"Alert image saved: {image_path}"
                    )

                    # =================================================
                    # FIREBASE
                    # =================================================

                    try:

                        firebase_result = upload_detection(
                            class_name=class_name,
                            confidence=confidence,
                            pole_id=POLE_ID,
                            image_path=image_path
                        )

                        if firebase_result:

                            print(
                                "Firebase event uploaded"
                            )

                        else:

                            print(
                                "Firebase upload skipped/failed"
                            )

                    except Exception as e:

                        print(
                            "Firebase error:",
                            e
                        )

                    # =================================================
                    # TELEGRAM
                    # =================================================

                    try:

                        telegram_result = send_telegram_alert(
                            class_name=class_name,
                            confidence=confidence,
                            pole_id=POLE_ID,
                            image_path=image_path
                        )

                        if telegram_result:

                            print(
                                "Telegram alert sent"
                            )

                        else:

                            print(
                                "Telegram alert failed"
                            )

                    except Exception as e:

                        print(
                            "Telegram error:",
                            e
                        )

                    # Update cooldown
                    last_alert_time = current_time

                    print(
                        "Alert cooldown started: 30 seconds"
                    )

            # =================================================
            # TOP INFORMATION
            # =================================================

            cv2.putText(
                annotated_frame,
                f"PRANSTHAMBH | {POLE_ID}",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (255, 255, 255),
                2
            )

            # =================================================
            # DISPLAY
            # =================================================

            cv2.imshow(
                "PRANSTHAMBH AI LIVE",
                annotated_frame
            )

            # Q = Quit
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):

                print("Stopping PRANSTHAMBH...")
                break

    except KeyboardInterrupt:

        print()
        print("System interrupted by user")

    finally:

        camera.release()

        cv2.destroyAllWindows()

        alert_manager.normal_state()

        print("PRANSTHAMBH stopped safely")


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    main()