import cv2
import numpy as np
import onnxruntime as ort
import os

# ---------------- CONFIG ----------------
MODEL_PATH = "get_leaves.onnx"
IMAGE_PATH = "leaves1.jpg"
OUTPUT_DIR = "extracted_leaves"

IMG_SIZE = 640
CONF_THRESHOLD = 0.4
IOU_THRESHOLD = 0.5
# ----------------------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load ONNX model
session = ort.InferenceSession(
    MODEL_PATH,
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# Load image
image = cv2.imread(IMAGE_PATH)
h_img, w_img, _ = image.shape

# -------- Preprocess --------
img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
img = img.astype(np.float32) / 255.0
img = np.transpose(img, (2, 0, 1))
img = np.expand_dims(img, axis=0)

# -------- Inference --------
outputs = session.run([output_name], {input_name: img})[0]
outputs = np.squeeze(outputs).T   # shape: (num_boxes, 6+)

boxes = []
scores = []

for det in outputs:
    conf = det[4]
    if conf < CONF_THRESHOLD:
        continue
    
    
    score = conf 

    if score < CONF_THRESHOLD:
        continue

    x, y, w, h = det[:4]

    # Convert to pixel coords
    x1 = int((x - w / 2) * w_img / IMG_SIZE)
    y1 = int((y - h / 2) * h_img / IMG_SIZE)
    x2 = int((x + w / 2) * w_img / IMG_SIZE)
    y2 = int((y + h / 2) * h_img / IMG_SIZE)

    boxes.append([x1, y1, x2, y2])
    scores.append(float(score))

# -------- NMS --------
indices = cv2.dnn.NMSBoxes(
    boxes,
    scores,
    CONF_THRESHOLD,
    IOU_THRESHOLD
)

# -------- Crop & Save --------
count = 0
for i in indices.flatten():
    x1, y1, x2, y2 = boxes[i]

    x1, y1 = max(0, x1), max(0, y1)
    x2, y2 = min(w_img, x2), min(h_img, y2)

    crop = image[y1:y2, x1:x2]

    if crop.size == 0:
        continue

    cv2.imwrite(
        os.path.join(OUTPUT_DIR, f"leaf_{count}.jpg"),
        crop
    )
    count += 1

print(f"[INFO] Extracted {count} leaves into '{OUTPUT_DIR}'")
