import cv2, pandas
from datetime import datetime

firstf=None
statuslist=[None,None]
time=[]
df=pandas.DataFrame(columns=["Start","End"])

video=cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status=0
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)

    if firstf is None:
        firstf=gray
        continue

    deltaf=cv2.absdiff(firstf,gray)
    threshf=cv2.threshold(deltaf,30,255, cv2.THRESH_BINARY)[1]
    threshf=cv2.dilate(threshf,None,iterations=2)

    (_,cnts,_)=cv2.findContours(threshf.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        (x,y,w,h)=cv2.boundingRect(contour)
        cv2.rectangle(frame, (x,y), (x+w, y+h),(255,0,0), 3)
    statuslist.append(status)

    if statuslist[-1] == 1 and statuslist[-2] == 0:
        time.append(datetime.now())
    if statuslist[-1] == 0 and statuslist[-2] == 1:
        time.append(datetime.now())

    cv2.imshow("Grey",gray)
    cv2.imshow("Delta",deltaf)
    cv2.imshow("Threshold",threshf)
    cv2.imshow("Color",frame)

    key=cv2.waitKey(1)

    if key == ord('q'):
        if status==1:
            time.append(datetime.now())
        break

for x in range(0,len(time), 2):
    df.append({"Start":time[x],"End":time[x+1]},ignore_index=True)

df.to_csv("time.csv")

video.release()
cv2.destroyAllWindows
