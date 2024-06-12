import cv2
import numpy as np
from pydarknet import Detector, Image
from dronekit import connect, VehicleMode

vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

net = Detector(bytes("yolov4.cfg", encoding="utf-8"), bytes("yolov4.weights", encoding="utf-8"), 0,
               bytes("coco.data", encoding="utf-8"))

# Initialize camera / movement_cmd
cap = cv2.VideoCapture(0)

def send_movement_command(error_x, error_y):
    #proportional control
    Kp = 0.1
    
    #control signals
    right = 1500 + error_x * Kp
    forward = 1500 - error_y * Kp

    # Ensure the commands are within safe bounds
    right = max(1000, min(2000, right))
    forward = max(1000, min(2000, forward))

    #Send thecommands to the drone
    vehicle.channels.overrides = {'1': right, '2': forward}

while True:
    ret, frame = cap.read()
    if not ret:
        break
   
    img_darknet = Image(frame)
    results = net.detect(img_darknet)

    for cat, score, bounds in results:
        x, y, w, h = bounds
        cx, cy = x + w / 2, y + h / 2

        #  name as necessary
        if cat.decode("utf-8") == "hotspot":
            # Calculate the error from the center of the image
            error_x = cx - frame.shape[1] / 2
            error_y = cy - frame.shape[0] / 2

            # Send movement commands to the drone - important
            send_movement_command(error_x, error_y)

    
    for cat, score, bounds in results:
        x, y, w, h = bounds
        cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (255, 0, 0), 2)
        cv2.putText(frame, cat.decode("utf-8"), (int(x), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()
vehicle.close()
