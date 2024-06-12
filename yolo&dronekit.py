import cv2
import numpy as np
from pydarknet import Detector, Image
from dronekit import connect, VehicleMode

# Connect to the drone
vehicle = connect('/dev/ttyUSB0', baud=57600, wait_ready=True)

# Load YOLO model
net = Detector(bytes("yolov4.cfg", encoding="utf-8"), bytes("yolov4.weights", encoding="utf-8"), 0,
               bytes("coco.data", encoding="utf-8"))

# Initialize the camera
cap = cv2.VideoCapture(0)
