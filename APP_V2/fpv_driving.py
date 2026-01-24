import cv2


cap = cv2.VideoCapture(0)

while True:
    _,img = cap.read()

    cv2.imshow("FPV Driving", img)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()