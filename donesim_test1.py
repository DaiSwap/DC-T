import cv2
import numpy as np
from DroneBlocksTelloSimulator.DroneBlocksSimulatorContextManager import DroneBlocksSimulatorContextManager
#from djitellopy import Tello
import time
sim_key = "56e0ac40-eadb-4b74-a140-0612bc4f1250"

img1 = ["1.1.jpeg","2.1.jpeg","3.1.jpeg","4.jpeg","5.jpeg","6.jpeg"]
def detect_circle(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (15, 15), 0)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, minDist=50, param1=100, param2=30, minRadius=10,
                               maxRadius=100)
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            return (x, y, r)
    return None


def calculate_offsets(circle_center, image_center):
    offset_x = circle_center[0] - image_center[0]
    offset_y = circle_center[1] - image_center[1]
    return offset_x, offset_y


def main():
    with DroneBlocksSimulatorContextManager(simulator_key=sim_key) as drone:
        drone.takeoff()
        time.sleep(2)  # Give time for the drone to stabilize
        image_center = (480, 360)  # Assuming 960x720 resolution
        i = 0
        while True:
            # Capture image from drone's camera
            #frame = drone.get_frame_read().frame

            frame = "Screenshot 2024-06-06 at 6.31.50 PM.png"
            if i < len(img1):
                image = cv2.imread(img1[i])
                i+=1

            # Detect circle
            circle = detect_circle(image)

            if circle is not None:
                offset_x, offset_y = calculate_offsets((circle[0], circle[1]), image_center)
                # Set a threshold for minimal movement to avoid oscillations
                threshold = 20
                distance = 20  # Move by 20 inches each time

                # Move drone based on offsets
                if abs(offset_y) > threshold:
                    if offset_y > 0:
                        drone.fly_forward(distance, 'in')
                    else:
                        drone.fly_backward(distance, 'in')

                if abs(offset_x) > threshold:
                    if offset_x > 0:
                        drone.fly_right(distance, 'in')
                    else:
                        drone.fly_left(distance, 'in')

            # Display the frame with detected circle for debugging
            if circle is not None:
                cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
                print("error")
            cv2.imshow("Drone Camera", image)


            # Break loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(1)  # Sleep for 1 second before next loop to allow for movement

        drone.land()
        cv2.destroyAllWindows()







if __name__ == "__main__":
    main()
