import onnxruntime as ort
import numpy as np
import cv2
import os
from PIL import Image

# ======================
# CONFIG
# ======================
IMG_SIZE = 224
CLASS_NAMES = ["blight", "healthy"]

INPUT_DIR = "captured_images"          # folder with images
OUTPUT_DIR = "annotated_results"    # output folder
ALLOWED_EXTS = (".jpg", ".jpeg", ".png")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ======================
# Load ONNX model
# ======================
session = ort.InferenceSession(
    "potato_leaf.onnx",
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name

# ======================
# Prediction function
# ======================
def predict_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))

    img_np = np.array(img).astype(np.float32) / 255.0
    img_np = np.expand_dims(img_np, axis=0)

    output = session.run(None, {input_name: img_np})[0][0]

    pred_idx = np.argmax(output)
    confidence = float(output[pred_idx])

    return CLASS_NAMES[pred_idx], confidence


# ======================
# Annotate all images
# ======================
for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(ALLOWED_EXTS):
        continue

    img_path = os.path.join(INPUT_DIR, filename)

    # Predict
    label, conf = predict_image(img_path)

    # Read image using OpenCV (for annotation)
    img = cv2.imread(img_path)
    if img is None:
        print(f"❌ Could not read {filename}")
        continue

    text = f"{label} ({conf*100:.1f}%)"

    # Color by class
    color = (0, 255, 0) if label == "healthy" else (0, 0, 255)

    # Background box
    (tw, th), _ = cv2.getTextSize(
        text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
    )
    cv2.rectangle(img, (5, 5), (10 + tw, 15 + th), (0, 0, 0), -1)

    # Put text
    cv2.putText(
        img,
        text,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
        cv2.LINE_AA
    )

    # Save annotated image
    out_path = os.path.join(OUTPUT_DIR, filename)
    cv2.imwrite(out_path, img)

    print(f"✅ {filename} → {label} ({conf:.3f})")

print("\n🎉 All images annotated and saved.")
