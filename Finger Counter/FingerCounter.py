import cv2
import time
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from HandTracker import HandTrackerModule as htm

detector =htm.HandDetector(detectionCon=0.75)
cap=cv2.VideoCapture(0)

# setting height and width of the camera
wCam=640
hCam=480

cap.set(3,wCam)
cap.set(4,hCam)
# ########################################
pTime=0

tipIds=[4,8,12,16,20]
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList =detector.findPosition(img,draw=False)  
    if len(lmList)!=0:
        fingers=[]
        for id in range(0,5):
            if lmList[tipIds[id]][2]<lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        print(fingers)

    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    
    
    cv2.imshow("Image",img)
    cv2.waitKey(1)
