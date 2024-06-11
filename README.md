A. Python script designed to control drone using the DroneKit library while simultaneously utilizing the YOLO model for real-time object detection.

B. 2D to 3D spatial mapping

### A.
1. **Library Imports:**
    - `cv2` (OpenCV): Used for capturing video from the camera and displaying it.
    - `numpy`: Image processing tasks.
    - `pydarknet`: A Python wrapper for the Darknet YOLO implementation, used for object detection.
    - `dronekit`: A library that allows communication and control of drones using the MAVLink protocol.

2. **Drone Connection:**
    - The drone is connected via a serial connection (usually over USB) using `dronekit.connect`.

3. **YOLO Model Loading:**
    - The YOLO model is loaded using the `Detector` class from `pydarknet`. Configuration files and weights are specified for the model.

4. **Camera Initialization:**
    - OpenCV is used to capture video from the default camera (`cv2.VideoCapture(0)`).

5. **Main Loop:**
    - The script enters a loop where it continuously captures frames from the camera.
    - Each frame is passed through the YOLO object detector to identify objects within the frame.

6. **Object Detection and Decision Making:**
    - For each detected object, if the object is classified as a "person," the script calculates the error in the x and y positions between the detected person’s center and the center of the frame.
    - A simple proportional controller calculates the forward and right movements needed to center the detected person in the frame.
    - These movements are then translated into control commands which are sent to the drone using `vehicle.channels.overrides`.

7. **Display and Cleanup:**
    - The frame with detections is displayed using OpenCV.
    - The loop continues until the 'q' key is pressed.
    - Finally, the script releases the camera, closes all OpenCV windows, and closes the connection to the drone.

# Purpose

The script aims to demonstrate a basic example of autonomous drone control based on real-time visual input. Specifically, it uses computer vision to detect a hotspot and adjusts the drone’s position to keep the hotspot centered in the camera's field of view.


### B.
2D image coordinates from YOLO detections into real-world coordinates using camera calibration data and a fixed altitude. Here's a more detailed explanation of how each part of your code works and how you can use this information to guide a drone:


1. **Loading Camera Calibration Data**:
   - `load_camera_calibration(file_path)`: This function loads the camera matrix (`mtx`) and distortion coefficients (`dist`) from a `.npz` file containing the camera calibration data.

2. **Image to World Coordinates Conversion**:
   - `image_to_world_coordinates(u, v, altitude, camera_matrix)`: This function converts the 2D image coordinates (u, v) to 3D world coordinates (X, Y) using the camera matrix and the altitude of the drone.
   - `uv_1 = np.array([u, v, 1.0])`: Homogeneous coordinates of the image point.
   - `normalized_coords = np.linalg.inv(camera_matrix).dot(uv_1)`: Normalizes the image coordinates using the inverse of the camera matrix.
   - `X = normalized_coords[0] * altitude` and `Y = normalized_coords[1] * altitude`: Scales the normalized coordinates by the drone's altitude to obtain real-world coordinates.

3. **Main Function**:
   - `main()`: Loads the camera calibration data, defines example image coordinates, sets a fixed altitude, and then converts the image coordinates to real-world coordinates. Finally, it prints the results.

# Using Coordinates to Guide the Drone

Now, to use these real-world coordinates to guide the drone, you can integrate this process with your drone control logic. Here’s how you can do it:

1. **Integrate with YOLO Detection**:
   - Replace the `u, v` coordinates with the actual coordinates from the YOLO detection results.

2. **Control Logic**:
   - Use the calculated real-world coordinates (`X`, `Y`) to generate movement commands for the drone.
   - For example, if `X` and `Y` indicate that the target is to the left and forward, send commands to move left and forward until the target is centered.

By integrating YOLO with camera calibration and control logic, you can effectively guide the drone towards detected hotspots or other objects of interest.
