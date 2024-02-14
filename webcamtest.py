import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    print("Error: Couldn't open webcam.")
    exit()

# Capture a frame
ret, frame = cap.read()

# If frame is captured successfully, save it
if ret:
    cv2.imwrite("captured_image.jpg", frame)
    print("Image captured successfully.")

# Release the webcam
cap.release()
