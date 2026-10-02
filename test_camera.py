import cv2
from ultralytics import YOLO

MODEL_PATH = "best.pt"

print("=" * 50)
print("PRANSTHAMBH AI CAMERA TEST")
print("=" * 50)

# Load trained model
model = YOLO(MODEL_PATH)

print("Model loaded successfully!")
print("Classes:", model.names)

# Start camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera could not be opened.")
    exit()

print("Camera started successfully.")
print("AI detection started.")
print("Press Q to exit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera frame error")
        break

    # AI detection
    results = model(
        frame,
        conf=0.50,
        verbose=False
    )

    # Draw AI detections
    annotated_frame = results[0].plot()

    # Status text
    cv2.putText(
        annotated_frame,
        "PRANSTHAMBH AI LIVE",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    cv2.imshow(
        "PRANSTHAMBH - AI Detection",
        annotated_frame
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

print("PRANSTHAMBH camera test stopped.")