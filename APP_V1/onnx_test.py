import onnxruntime as ort
import numpy as np
from PIL import Image
import os
IMG_SIZE = 224
CLASS_NAMES = ["blight", "healthy", "other"]

print(os.listdir('/home/cypher/testvenv2/files/captured_images'))

# Load ONNX model
session = ort.InferenceSession(
    "potato_leaf.onnx",
    providers=["CPUExecutionProvider"]
)

input_name = session.get_inputs()[0].name

def predict(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE))

    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    output = session.run(None, {input_name: img})[0]
    pred = np.argmax(output)
    
    if output[0][0] < 0.98 and output[0][1] <0.98:
        print("Invalid Image provided, try again nerd!")
        pred = 2
        output = None
    print(f"Prediction: {CLASS_NAMES[pred]}")
    print("Raw scores:", output)

# TEST
#predict("healthy.jpg")
#predict("blight.jpg")
#predict("ball.jpg")
#predict("suiii.jpg")

#predict("images.jpg")
#predict("images2.jpg")




for i in os.listdir('/home/cypher/testvenv2/files/captured_images'):
    predict(f'/home/cypher/testvenv2/files/captured_images/{i}')