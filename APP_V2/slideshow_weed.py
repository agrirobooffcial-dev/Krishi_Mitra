import cv2
import os

# ======================
# CONFIG
# ======================
IMAGE_DIR = "detections"
ALLOWED_EXTS = (".jpg", ".jpeg", ".png")

BUTTON_W, BUTTON_H = 150, 50
BUTTON_MARGIN = 20

# ======================
# LOAD IMAGES
# ======================
images = [
    os.path.join(IMAGE_DIR, f)
    for f in sorted(os.listdir(IMAGE_DIR))
    if f.lower().endswith(ALLOWED_EXTS)
]

if not images:
    raise RuntimeError("No images found in output directory")

index = 0
current_img = None


# ======================
# MOUSE CALLBACK
# ======================
def mouse_handler(event, x, y, flags, param):
    global index

    if event == cv2.EVENT_LBUTTONDOWN:
        h, w = current_img.shape[:2]

        bx1 = w - BUTTON_W - BUTTON_MARGIN
        by1 = h - BUTTON_H - BUTTON_MARGIN
        bx2 = w - BUTTON_MARGIN
        by2 = h - BUTTON_MARGIN

        if bx1 <= x <= bx2 and by1 <= y <= by2:
            index = (index + 1) % len(images)


cv2.namedWindow("Slideshow")
cv2.setMouseCallback("Slideshow", mouse_handler)

# ======================
# MAIN LOOP
# ======================
print("Press Escape to exit :)")
while True:
    img = cv2.imread(images[index])
    if img is None:
        index = (index + 1) % len(images)
        continue

    current_img = img.copy()
    h, w = current_img.shape[:2]

    # Draw NEXT button
    bx1 = w - BUTTON_W - BUTTON_MARGIN
    by1 = h - BUTTON_H - BUTTON_MARGIN
    bx2 = w - BUTTON_MARGIN
    by2 = h - BUTTON_MARGIN

    cv2.rectangle(current_img, (bx1, by1), (bx2, by2), (50, 50, 50), -1)
    cv2.rectangle(current_img, (bx1, by1), (bx2, by2), (255, 255, 255), 2)

    cv2.putText(
        current_img,
        "NEXT",
        (bx1 + 35, by1 + 33),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2
    )

    # Image counter


    cv2.imshow("Slideshow", current_img)

    key = cv2.waitKey(20)
    if key == 27:  # ESC
        break

cv2.destroyAllWindows()
