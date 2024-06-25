import cv2

def capture_image(save_path):
    # Open the camera
    cap = cv2.VideoCapture(0)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Failed to open the camera")
        return

    # Capture a frame from the camera
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Failed to capture frame")
        return

    # Save the image to the given path
    cv2.imwrite(save_path, frame)
    print("Picture clicked and saved photo.")

    # Release the camera
    cap.release()

# Specify the path to save the image
save_path = r"D:\RAO\IoT\IOT project\photos\new_person.jpg"

# Call the capture_image function
capture_image(save_path)
