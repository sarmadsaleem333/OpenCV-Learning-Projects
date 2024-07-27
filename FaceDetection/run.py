from FaceDetectionModule import FaceDetector
import cv2
import time

cap=cv2.VideoCapture(0)
pTime=0
detector=FaceDetector()
while True:
    success,img=cap.read()
    img,boxes=detector.findFaces(img)
    print(boxes)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(20,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    cv2.imshow("Image",img)
    cv2.waitKey(1)