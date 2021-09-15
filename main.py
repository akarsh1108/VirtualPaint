import cv2
import numpy as np
cap=cv2.VideoCapture(0)
# for height with and brightness
cap.set(8,1080)
cap.set(7,960)
cap.set(10,100)

myColors =[[121,11,255,179,255,255],
           [35,32,185,90,255,255],
           [69,115,202,110,255,255]]
myColorsValues=[[152,56,255],
                [5,239,155],
                [200,142,67]]

myPoints =[]#[x,y,colorID
newPoints=[]
def findcolor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0;
    for color in myColors:
       lower=np.array(color[0:3])
       upper=np.array(color[3:6])
       mask = cv2.inRange(imgHSV, lower, upper)
       x,y=getContours(mask)
       cv2.circle(imgResult,(x,y),5,myColorValues[count],cv2.FILLED)
       if x!=0 and y!=0:
           newPoints.append([x,y,count])
       count +=1
       # cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>500:
            # draw the contour img contour cnt(contour) index
            # cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri=cv2.arcLength(cnt,True)
            approx=cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h=cv2.boundingRect(approx)
        #     this will give us the top point and the tip point as well
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult,(point[0],point[1]),10,myColorValues[point[2]],cv2.FILLED)
while True:
    success,img=cap.read()
    imgResult=img.copy()
    newPoints=findcolor(img,myColors,myColorsValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorsValues)
    cv2.imshow("Video",imgResult)
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break