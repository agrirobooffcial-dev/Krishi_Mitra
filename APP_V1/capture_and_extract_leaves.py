import cv2
import numpy as np
import onnxruntime as ort
import os
import time

# ---------------- CONFIG ----------------
MODEL_PATH = "get_leaves.onnx"
CAPTURE_DIR = "captured_frames"
OUTPUT_DIR = "extracted_leaves"

IMG_SIZE = 640
CONF_THRESHOLD = 0.4
IOU_THRESHOLD = 0.5
CAPTURE_INTERVAL = 5  # seconds
CAMERA_INDEX = 0
# ----------------------------------------

os.makedirs(CAPTURE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load ONNX model
session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Open webcam
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    raise RuntimeError("Could not open webcam")

print("[INFO] Webcam started. Press Ctrl+C to stop.")

frame_id = 0

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARN] Failed to grab frame")
            continue

        timestamp = int(time.time())
        frame_name = f"frame_{frame_id}_{timestamp}.jpg"
        frame_path = os.path.join(CAPTURE_DIR, frame_name)

        # Save raw frame
        cv2.imwrite(frame_path, frame)
        print(f"[INFO] Captured {frame_name}")

        h_img, w_img, _ = frame.shape

        # -------- Preprocess --------
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        img = img.astype(np.float32) / 255.0
        img = np.transpose(img, (2, 0, 1))
        img = np.expand_dims(img, axis=0)

        # -------- Inference --------
        outputs = session.run([output_name], {input_name: img})[0]
        outputs = np.squeeze(outputs)

        boxes = []
        scores = []

        for det in outputs:
            conf = det[4]
            if conf < CONF_THRESHOLD:
                continue

            x, y, w, h = det[:4]

            x1 = int((x - w / 2) * w_img / IMG_SIZE)
            y1 = int((y - h / 2) * h_img / IMG_SIZE)
            x2 = int((x + w / 2) * w_img / IMG_SIZE)
            y2 = int((y + h / 2) * h_img / IMG_SIZE)

            boxes.append([x1, y1, x2, y2])
            scores.append(float(conf))

        # -------- NMS --------
        indices = cv2.dnn.NMSBoxes(
            boxes,
            scores,
            CONF_THRESHOLD,
            IOU_THRESHOLD
        )

        leaf_count = 0
        if len(indices) > 0:
            for i in indices.flatten():
                x1, y1, x2, y2 = boxes[i]

                x1, y1 = max(0, x1), max(0, y1)
                x2, y2 = min(w_img, x2), min(h_img, y2)

                crop = frame[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                leaf_name = f"leaf_{frame_id}_{leaf_count}.jpg"
                cv2.imwrite(os.path.join(OUTPUT_DIR, leaf_name), crop)
                leaf_count += 1

        print(f"[INFO] Extracted {leaf_count} leaves")

        frame_id += 1
        time.sleep(CAPTURE_INTERVAL)

except KeyboardInterrupt:
    print("\\n[INFO] Stopping...")

finally:
    cap.release()
    cv2.destroyAllWindows()
