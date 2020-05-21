"""
This is a motion detector created using opencv a python library used for image processing. This program detects objects through the webcam.
The image is converted to a gray scale image and blurred to reduce the noise in the image. The difference between the first frame and the second 
is then obtained to detect movement. The difference is converted to its binary form for processing and then contours are then drawn around the object 
based on the area of the object and a rectangle around the contour is then drawn to define the position of the object.
"""

# importing relevant libraries
import cv2, pandas
from datetime import datetime

# creating variables to store certain values
# Creating the first frame variable ie. the first frame to be captured when the program is first run
firstf=None
# This stores te change in motion caught by the webcam
statuslist=[None,None]
# Stores the time values where motion is detected
time=[]
# Creating a dataframe to store the values from the time variable
df=pandas.DataFrame(columns=["Start","End"])
# Starting the webcam, creating a video variable to store the video and declaring which webcam to use incase of mutiple webcams
video=cv2.VideoCapture(0)

# This keeps the webcam on until it is stopped manually
while True:
    # Videos are many pictures that are put together and therefore this is obtaining every picture frame recorded and declaring it as a variable
    check, frame = video.read()
    # This variable is to state that until this point no motion has been recorded
    status=0
    # converting the picture frame to grayscale
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # blurring the grayscale image to reduce noise from the images
    gray=cv2.GaussianBlur(gray,(21,21),0)

    # conditional to check whether the first frame has been assigned a value. If not it is assigned the image being parsed to be first frame else 
    # it goes back to the beginning of the while loop
    if firstf is None:
        firstf=gray
        continue
    
    # finding the difference between the first frame and the current frame being parsed
    deltaf=cv2.absdiff(firstf,gray)
    # Getting a binary image out of the difference of the above mentioned images known as a threshold image. When the difference between 
    # the pixels of an image area where motion has been detected is greater than 30 it is converted to white ie. 255
    threshf=cv2.threshold(deltaf,30,255, cv2.THRESH_BINARY)[1]
    # dilate function then smoothens the threhhold image. Iterations are the number of times the threshold image will be smoothened and 
    # if a threshold kernel was available it would be parsed where there is none
    threshf=cv2.dilate(threshf,None,iterations=2)

    # Finding the difference in shapes and objects in the binary image ie. threshold image. We use the copy of the threshold image 
    # to avoid altering the real threshold image and the mode and method are then parsed on how to define the contours
    (cnts,_)=cv2.findContours(threshf.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # Using the contours we can determine whether motion or an object has been detected based on the area of the contours. If greater than
    # 10,000 status changes to 1 showing motion else it goes back to the beginning of the while loop
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status=1

        # Drawing a rectangle aroung the object that has been identified through the contours. x & y are coordinates of the top left corner
        # of the rectangle, w & h are its width and height
        (x,y,w,h)=cv2.boundingRect(contour)
        # Here we parse in the coordinates, color and the thickness of the rectangle
        cv2.rectangle(frame, (x,y), (x+w, y+h),(255,0,0), 3)

    # appending the status values to the statuslist variable
    statuslist.append(status)

    # conditionals to determine and record the time an object is detected and when it gets out of the frame. The times are then
    # appended to the time variable 
    if statuslist[-1] == 1 and statuslist[-2] == 0:
        time.append(datetime.now())
    if statuslist[-1] == 0 and statuslist[-2] == 1:
        time.append(datetime.now())
        
    # showing the video based on the different frames created from the colored,grayscale,difference and threshold images
    cv2.imshow("Grey",gray)
    cv2.imshow("Delta",deltaf)
    cv2.imshow("Threshold",threshf)
    cv2.imshow("Color",frame)

    # Time period the window used to show the frames should show
    key=cv2.waitKey(1)

    # Conditional that allows exit of the program by pressing 'q'
    if key == ord('q'):
        if status==1:
            time.append(datetime.now())
        break

# Appending the time data to the dataframe
for x in range(0,len(time), 2):
    df=df.append({"Start":time[x],"End":time[x+1]},ignore_index=True)

# exporting the dataframe in csv format
df.to_csv("time.csv")

# This releases the webcam from the program
video.release()
# destroys all the windows created by the program
cv2.destroyAllWindows
