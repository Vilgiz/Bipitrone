import cv2
import numpy
import cvzone

cap = cv2.VideoCapture("Datasets/video_1.mp4")

while (True):
    ret, frame = cap.read()
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
    weight = int(1920/2)
    height = int(1080/2)
    cv2.resizeWindow('Video', weight, height)

    cv2.imshow("Video", frame)
    
    cv2.waitKey(int(1000/(60)))
        


        

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
    