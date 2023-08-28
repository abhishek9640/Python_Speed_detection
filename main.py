import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tracker import*
import time

model = YOLO('yolov8m.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

cap = cv2.VideoCapture('test.mp4')

my_file = open("coco.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0
tracker = Tracker()
cy1 = 171
cy2 = 282
offset = 5
vh_up = {}
time_list = []

# frame_rate = 25  # Desired frame rate (frames per second)
# frame_delay = 0.00001

while True:    
    ret, frame = cap.read()
    if not ret:
        break
    count += 1
    if count % 2 != 0:
        continue
    frame = cv2.resize(frame, (1020, 500))

    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")
    list = []

    for index, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])
        c = class_list[d]
        if 'car' in c:
            list.append([x1, y1, x2, y2])
    bbox_id = tracker.update(list)
    
    for bbox in bbox_id:
        x3, y3, x4, y4, id = bbox
        cx = int((x3 + x4) // 2)
        cy = int((y3 + y4) // 2)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        if cy > cy1 - offset and cy < cy1 + offset:
            cv2.putText(frame, str("THIS CAR CROSSED LINE 1"), (cx, cy - 15), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)
            print("THIS CAR CROSSED LINE 1")
            t1 = time.time()
            print("t1 value is " + str(t1))
            time_list.append(t1)
        if cy > cy2 - offset and cy < cy2 + offset:
            cv2.putText(frame, str("THIS CAR CROSSED LINE 2"), (cx, cy - 15), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 1)
            print("THIS CAR CROSSED LINE 2")
            t2 = time.time()
            print("t2 value is " + str(t2))
            time_list.append(t2)

    if len(time_list) == 2:
        print(time_list)
        distance = 10  # Meters
        if time_list[1] > time_list[0]:
            time1 = time_list[1] - time_list[0]
        elif time_list[0] > time_list[1]:
            time1 = time_list[0] - time_list[1]
        speed_kmh = (distance / time1) * 3.6
        print("********Speed is: ", speed_kmh, "km/hr*********")

        # You can capture the calculated speed and save it to a file or a variable
        with open("speed_log.txt", "a") as speed_file:
            speed_file.write(f"Speed: {speed_kmh} km/hr\n")

        time_list = []

    cv2.line(frame, (306, cy1), (800, cy1), (255, 255, 255), 1)
    cv2.line(frame, (196, cy2), (900, cy2), (255, 255, 255), 1)
    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

    # time.sleep(frame_delay)

cap.release()
cv2.destroyAllWindows()
