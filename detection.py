import cv2
from ultralytics import YOLO
from config import MODEL_PATH, CONFIDENCE_THRESHOLD


class PransthambhDetector:

    def __init__(self):

        print("=" * 50)
        print("Loading PRANSTHAMBH AI Model...")
        print("=" * 50)

        self.model = YOLO(MODEL_PATH)

        print("Model loaded successfully")
        print("Classes:", self.model.names)

    def detect(self, frame):

        results = self.model(
            frame,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])
                confidence = float(box.conf[0])

                class_name = self.model.names[class_id]

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                detections.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": [x1, y1, x2, y2]
                })

        return detections

    def draw_detections(self, frame, detections):

        for detection in detections:

            x1, y1, x2, y2 = detection["bbox"]

            class_name = detection["class_name"]
            confidence = detection["confidence"]

            confidence_percent = confidence * 100

            label = (
                f"{class_name} "
                f"{confidence_percent:.1f}%"
            )

            # Bounding box
            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 0, 255),
                2
            )

            # Label background
            (text_width, text_height), baseline = cv2.getTextSize(
                label,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                2
            )

            label_y = max(y1, text_height + 10)

            cv2.rectangle(
                frame,
                (x1, label_y - text_height - 10),
                (x1 + text_width + 10, label_y),
                (0, 0, 255),
                -1
            )

            # Label text
            cv2.putText(
                frame,
                label,
                (x1 + 5, label_y - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )

        return frame