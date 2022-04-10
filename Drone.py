from djitellopy import tello
import cv2 as cv
import numpy as np
import time

def findFace(drone, haar_cascade, enableFallowFace, camera):
    gray = cv.cvtColor(camera, cv.COLOR_BGR2GRAY) #gray
    faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors=8)

    for (x,y,w,h) in faces_rect:
        cv.rectangle(camera, (x,y), (x+w, y+h), (0,255,0), thickness=2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        print (area)

        if (enableFallowFace == True):

            width, height = camera.shape[:2]
            width = int(width // 2)
            height = int(height // 2)

            if (int(cy) > int(height)):
                print("drone move_down ", cy, height)
                #drone.move_down(20)
                #time.sleep(1)
            elif (int(cy) < int(height)):
                print("drone move_up ", cy, height)
                #drone.move_up(20)
                #time.sleep(1)

            if (area < 2000):
                #drone.send_rc_control(0, 20, 0, 50)
                drone.move_forward(100)
                #time.sleep(0.3)
            elif(area > 3000):
                #drone.send_rc_control(0, -20, 0, -50)
                drone.move_back(100)
                #time.sleep(0.3)

            
def main():
    width = 320
    height = 240
    testMode = 0
    enableStream = True
    enableFindFace = True
    enableFallowFace = True

    drone = tello.Tello()
    drone.connect()
    drone.speed = 0

    print(drone.get_battery())

    if testMode == 1:
        drone.takeoff()
        time.sleep(1)
        drone.send_rc_control(0, 20, 0, 0)
        time.sleep(1)
        drone.flip_forward()
        time.sleep(0)
        drone.land()

    if enableStream == True:
        drone.streamon()
        time.sleep(5)
        drone.takeoff()

        while True:
            frame = drone.get_frame_read().frame
            stream = cv.resize(frame, (width, height))
            cv.imshow('Tello drone', stream)

            if cv.waitKey(20) & 0xFF == ord('d'):
                drone.land()
                break
            if cv.waitKey(20) & 0xFF == ord('t'):
                drone.takeoff()
                break

            if (enableFindFace == True):
                haar_cascade = cv.CascadeClassifier('haar_face.xml')
                cv.circle(stream, ((height // 2), (width // 2)), 3, (255,255,0), cv.FILLED)
            
                if enableFindFace == True:
                    findFace(drone, haar_cascade, enableFallowFace, stream)

main()

