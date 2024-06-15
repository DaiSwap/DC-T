import numpy as np

def load_camera_calibration(file_path):
    with np.load(file_path) as data:
        mtx = data['mtx']
        dist = data['dist']
    return mtx, dist

def image_to_world_coordinates(u, v, altitude, camera_matrix):
    
    uv_1 = np.array([u, v, 1.0])
    normalized_coords = np.linalg.inv(camera_matrix).dot(uv_1)
    
    
    X = normalized_coords[0] * altitude
    Y = normalized_coords[1] * altitude

    return X, Y

def main():
    
    camera_matrix, dist_coeffs = load_camera_calibration('camera_calibration.npz')

    # Example 2D image coordinates (center of the bounding box)
    u, v = 320, 240  # Change this to your actual coordinates from YOLO detection

    # Fixed altitude of the drone
    altitude = 15.0  # meters

    
    X, Y = image_to_world_coordinates(u, v, altitude, camera_matrix)

    print(f"Real-world coordinates: X = {X}, Y = {Y}")

if __name__ == "__main__":
    main()
