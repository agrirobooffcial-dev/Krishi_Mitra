import cv2
import time
import os
import requests
from ultralytics import YOLO
from datetime import datetime
import serial
import time
import logging
import json


current = datetime.now()
os.system("sudo fuser -k /dev/video0")

with open("events4.log", "+w") as file1:
    file1.write("")
    

logging.basicConfig(
    filename = "events4.log",
    level = logging.INFO,
    format = "%(asctime)s - %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S"
    )


# Adjust the port based on your Pi (check with ls /dev/tty*)
# For Arduino Uno it’s often /dev/ttyACM0 or /dev/ttyUSB0
#arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

print("Connected to Arduino")
logging.info(f"Modules loaded!")

#def move_arm(position):
 #   if position in range(1, 4):
 #       arduino.write(str(position).encode())
  #      print(f"Sent position {position}")
  #      time.sleep(0.5)
   # else:
    #    print("Invalid position number (1–3)")





# -----------------------------
# Setup
# -----------------------------
model = YOLO('//home//cypher//testvenv2//plant_model.onnx', task='detect')
cap = cv2.VideoCapture(0)

classes_dict = {'0': 'weed1', '1': 'weed2', '2': 'weed3', '3': 'weedu','4':'weed4'}
target = ['weed1','weed2','weed3','weedu','weed4']

SAVE_DIR = "detections"
os.makedirs(SAVE_DIR, exist_ok=True)

DETECTION_INTERVAL = 7  # seconds
last_detection_time = 0
targets_detected = []

print("Starting detection loop... Press 'q' to exit.")
logging.info("Detection loop has started...")
logging.info("Looks like everything worked!")
#move_arm(1)

with open("data.json", "r") as f1:
    data = json.load(f1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    img = frame.copy()
    height, width, _ = img.shape
    part_width = width // 3  # 3 vertical parts

    # Draw 3 vertical sections
    for i in range(3):
        x1 = i * part_width
        x2 = (i + 1) * part_width
        cv2.rectangle(img, (x1, 0), (x2, height), (255, 255, 255), 2)
        cv2.rectangle(img, (x1 + 10, 10), (x1 + 180, 50), (0, 0, 0), -1)
        cv2.putText(img, f"Part {i + 1}", (x1 + 20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Run YOLO every few seconds
    current_time = time.time()
    if current_time - last_detection_time >= DETECTION_INTERVAL:
        last_detection_time = current_time
        results = model(frame)
        
        # Handle detections
        for box, cls in zip(results[0].boxes.xyxy, results[0].boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (cx, cy), 5, (128, 0, 128), -1)

            label = classes_dict.get(str(int(cls)), str(int(cls)))
            if label in target:
                col = cx // part_width
                part_number = min(col + 1, 3)  # ensure within 1–3
                #move_arm(int(part_number))
                #move_arm(1)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")
                cv2.imwrite(image_path, frame)
                print(f"[INFO] Frame saved: {image_path}")

                print(f"{label} detected in Part {part_number}")
                #cv2.putText(img, f'{label} - Part {part_number}', (x1, y1 - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

   
                targets_detected.append(label)
                data[label] += 1
                with open("//home//cypher//testvenv2//data.json", "+w") as f2:
                    json.dump(data, f2, indent = 1)
    # Show video feed (grid always visible)
    cv2.imshow("Live Detection", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#cap.release()
#cv2.destroyAllWindows()
print("Detection stopped.")

