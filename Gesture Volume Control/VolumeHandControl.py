import cv2 
import time
import numpy as np
import sys
import os
import math
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from HandTracker import HandTrackerModule as htm

from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volumeRange=volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-20.0, None)
maxVol=volumeRange[1]
minVol=volumeRange[0]

vol=0
volBar=400
cap=cv2.VideoCapture(0)

# setting height and width of the camera
wCam=640
hCam=480
cap.set(3,wCam)
cap.set(4,hCam)
# ########################################

pTime=0

detector =htm.HandDetector(detectionCon=0.7)

while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)
    if len(lmList)!=0:
        x1,y1=lmList[4][1],lmList[4][2]
        x2,y2=lmList[8][1],lmList[8][2]   
        cx,cy=(x1+x2)//2,(y1+y2)//2
        cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),10  ,(255,0,255),cv2.FILLED)
        length=math.hypot(x2-x1,y2-y1)
        print(length)
        # hand range 50- 300
        # volume range -65 - 0

        vol=np.interp(length,[50,300],[minVol,maxVol])
        volBar=np.interp(length,[50,300],[400,150])
        volume.SetMasterVolumeLevel(vol, None)     
        
        if length<50:
            cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
        cv2.rectangle(img,(50,150),(85,400),(0,255,0),3)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)

        
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.waitKey(1)
    cv2.imshow("Image",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


