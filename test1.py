import numpy as np
import cv2

# Create a black image
img = np.zeros((512, 512, 3), np.uint8)

# Display the image in a window
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
