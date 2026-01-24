from flask import Flask, render_template, request
import onnxruntime as ort
import numpy as np
import cv2
import os
from PIL import Image

app = Flask(__name__)

# Load ONNX model
MODEL_PATH = "potato2_leaf.onnx"
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# CHANGE THESE TO MATCH YOUR MODEL
CLASS_NAMES = ["blight", "healthy", "other"]

UPLOAD_FOLDER = "static/results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def preprocess_image(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img = np.array(img).astype(np.float32)
    img = img / 255.0            # Normalize
    img = np.expand_dims(img, 0) # Shape: (1, 224, 224, 3)
    return img

def annotate_image(image_path, label):
    img = cv2.imread(image_path)
    cv2.rectangle(img, (10, 10), (600, 80), (0, 0, 0), -1)
    cv2.putText(
        img,
        f"Identified {label}",
        (20, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.5,
        (0, 255, 0),
        3
    )
    return img

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]
        if file:
            input_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(input_path)

            input_tensor = preprocess_image(input_path)

            outputs = session.run(
                [output_name],
                {input_name: input_tensor}
            )

            pred_index = int(np.argmax(outputs[0]))
            predicted_class = CLASS_NAMES[pred_index]

            result_img = annotate_image(input_path, predicted_class)
            result_path = os.path.join(UPLOAD_FOLDER, "result_" + file.filename)
            cv2.imwrite(result_path, result_img)

            return render_template(
                "index.html",
                original_image=input_path,
                result_image=result_path,
                prediction=predicted_class
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
