import os
import time
from datetime import datetime

from config import (
    GREEN_LED_PIN,
    RED_LED_PIN,
    BUZZER_PIN,
    ALERTS_FOLDER,
    EVENTS_FOLDER,
    POLE_ID
)

import RPi.GPIO as GPIO


class AlertManager:

    def __init__(self):

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
        GPIO.setup(RED_LED_PIN, GPIO.OUT)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)

        os.makedirs(ALERTS_FOLDER, exist_ok=True)
        os.makedirs(EVENTS_FOLDER, exist_ok=True)

        self.normal_state()

    def normal_state(self):

        GPIO.output(GREEN_LED_PIN, GPIO.HIGH)
        GPIO.output(RED_LED_PIN, GPIO.LOW)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def alert_state(self):

        GPIO.output(GREEN_LED_PIN, GPIO.LOW)
        GPIO.output(RED_LED_PIN, GPIO.HIGH)

        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def save_event(self, detection):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        event_file = os.path.join(
            EVENTS_FOLDER,
            "events.txt"
        )

        with open(event_file, "a") as f:

            f.write(
                f"{timestamp} | "
                f"Pole={POLE_ID} | "
                f"Class={detection['class_name']} | "
                f"Confidence={detection['confidence']:.2f}\n"
            )