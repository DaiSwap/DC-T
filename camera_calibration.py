import numpy as np
import cv2
import glob

# Define chessboard size
chessboard_size = (8, 6)  # Adjust based on your actual chessboard

# Prepare object points
objp = np.zeros((np.prod(chessboard_size), 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

# Find chessboard corners in images
images = glob.glob('/home/pv/DCT/images/left_*.jpg')  # Path to your chessboard images
objpoints = []  # 3D points in real world space
imgpoints = []  # 2D points in image plane

if len(images) == 0:
    print("No images found. Check the file path and pattern.")
else:
    for fname in images:
        print(f"Processing {fname}")
        img = cv2.imread(fname)

        if img is None:
            print(f"Failed to load image {fname}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)  # Display each image for a short time
        else:
            print(f"Chessboard corners not found in {fname}")

    # Calibrate the camera if we have valid points
    if len(objpoints) > 0 and len(imgpoints) > 0:
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        # Save calibration results
        np.savez('camera_calibration.npz', mtx=mtx, dist=dist)

        # Print calibration results
        print("Camera matrix:\n", mtx)
        print("Distortion coefficients:\n", dist)
    else:
        print("Not enough points for calibration. Check your images and calibration setup.")

# Cleanup
cv2.destroyAllWindows()
