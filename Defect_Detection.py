# import libraries of python OpenCV  
# where its functionality resides 
import cv2  
import RPi.GPIO as GPIO
import time
from time import sleep
# np is an alias pointing to numpy library 
import numpy as np 
in1 = 15
in2 = 18
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

GPIO.output(in1, True)
GPIO.output(in2, True)
GPIO.output(11,GPIO.HIGH)
GPIO.output(12,GPIO.LOW)
# capture frames from a camera 
cap = cv2.VideoCapture(0)  
# loop runs if capturing has been initialized 
while(1): 
    # reads frames from a camera 
    ret, frame = cap.read() 
    # converting BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    
    # define range of red color in HSV 
    lower_red = np.array([30,150,50]) 
    upper_red = np.array([255,255,180])    
    # create a red HSV colour boundary and  
    # threshold HSV image 
    mask = cv2.inRange(hsv, lower_red, upper_red) 
    # Bitwise-AND mask and original image 
    res = cv2.bitwise_and(frame,frame, mask= mask) 
    # Display an original image 
    cv2.imshow('Original',frame) 
    # finds edges in the input image image and 
    # marks them in the output map edges 
    edges = cv2.Canny(frame,100,200)
    #to see if the matrix is all zeros
    canny_arr = np.array(edges)
    canny_flat = canny_arr.flatten()
    if np.count_nonzero(canny_flat)>50:
        print(np.count_nonzero(canny_flat))
        #print("LED on")
        GPIO.output(11,GPIO.LOW)
        GPIO.output(12,GPIO.HIGH)
        print("Damaged")
        print ("STOP")
        GPIO.output(in1, True)
        GPIO.output(in2, True)
        #print("stop")
        cv2.imwrite("Error.png",frame)
        break
    else:
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(12,GPIO.LOW)
        print(np.count_nonzero(canny_flat))
        #print("LED off")
        GPIO.output(in2, False)
        GPIO.output(in1, False)
        print("Continue")
        #print("start")
    # Display edges in a frame 
    cv2.imshow('Edges',edges) 
  
    # Wait for Esc key to stop 
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        GPIO.output(11,GPIO.LOW)
        GPIO.output(12,GPIO.LOW)
        GPIO.cleanup()
        break
# Close the window 
cap.release() 
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()  
