import cv2
import time

from PoseEstimationModule import PoseDetector

cap = cv2.VideoCapture(0)
pTime = 0
detector = PoseDetector()

while True:
    success, img = cap.read()
    if not success:
        break

    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[0])

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


   