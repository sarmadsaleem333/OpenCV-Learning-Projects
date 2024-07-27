import mediapipe as mp 
import time 
import cv2 
class FaceDetector:
    def __init__ (self,minDetectionCon=0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection=mp.solutions.face_detection
        self.face_detection=self.mpFaceDetection.FaceDetection(0.75)
        self.mpDraw=mp.solutions.drawing_utils
        self.results=None
    def findFaces(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        boxes=[]
        self.results=self.face_detection.process(imgRGB)
        if self.results.detections:
            if draw:
                for id,detection in enumerate (self.results.detections):
                    bboxC=detection.location_data.relative_bounding_box
                    ih,iw,ic=img.shape
                    bbox=int(bboxC.xmin*iw),int(bboxC.ymin*ih),int(bboxC.width*iw),int(bboxC.height*ih)
                    boxes.append([id,bbox,detection.score])
                    cv2.rectangle(img,bbox,(255,0,255),2)
                    cv2.putText(img,f'{int(detection.score[0]*100)}%',(bbox[0],bbox[1]-20),cv2.FONT_HERSHEY_PLAIN,2,(255,0,255),2)  
        return img,boxes

def main():
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
if __name__ == "__main__":
        main()
