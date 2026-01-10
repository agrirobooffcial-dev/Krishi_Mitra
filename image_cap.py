import cv2
import os
import time

# Create folder to save images
save_dir = "captured_images"
os.makedirs(save_dir, exist_ok=True)

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Cannot access webcam")
    exit()

print("📷 Capturing images every 5 seconds. Press 'q' to quit.")

last_capture_time = time.time()
img_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame")
        break

    # Show live camera feed
    cv2.imshow("Webcam", frame)

    current_time = time.time()

    # Capture image every 5 seconds
    if current_time - last_capture_time >= 5:
        img_count += 1
        filename = f"image_{img_count}.jpg"
        filepath = os.path.join(save_dir, filename)

        cv2.imwrite(filepath, frame)
        print(f"✅ Saved {filepath}")

        last_capture_time = current_time

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
