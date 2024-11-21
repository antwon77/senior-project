import cv2
import tkinter as tk
from tkinter import messagebox

def show_alert():
    """Create a UI alert when the video feed drops."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showerror("Camera Error", "The video feed has been lost. Please check the connection.")
    root.destroy()

def capture_video(camera_index=0):
    """
    Parameters:
    - camera_index: Index of the camera to be used (0 for default camera, like 1,2 or an index corresponding to a connected webcam or phone).
    If you want to switch from the iPhone to another camera (like a built-in webcam), (most likey gonna be 1-2 cause our camera will be plugged in as well)
    change the `camera_index` value when calling this function.
    """
    # Try to open the camera based on the index provided
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is successfully opened
    if not cap.isOpened():
        show_alert()  # Trigger an alert if the camera cannot be accessed
        return None

    # Set the best available resolution (you can adjust this based on your needs)
    #Full HD (1920x1080) is a good balance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set camera resolution width (change if needed)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set camera resolution height (change if needed)

    # Request the highest frame rate that the camera can handle,
    cap.set(cv2.CAP_PROP_FPS, 60)  # Set frame rate 

    # Read back the actual settings from the camera to confirm they were applied
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Print camera resolution and frame rate for debugging/confirmation purposes
    print(f"Camera Resolution: {int(width)}x{int(height)}")
    print(f"Camera Frame Rate: {fps} FPS")

    return cap  # Return the camera capture object for use in other parts of the program

def read_frame(cap):
    """
    Read a single frame from the video stream and check for errors.

    Parameters:
    - cap: The camera capture object returned by `capture_video()`.

    If the feed drops or the frame cannot be read, the program will trigger an alert and exit.
    """
    ret, frame = cap.read()  # Try to read a frame from the camera feed
    if not ret:
        print("Error: Could not read frame from camera feed.")  # Log an error message
        show_alert()  # Show an alert if the feed drops
        release_video(cap)  # Release the camera resources
        exit()  # Exit the program 
    return frame  # Return the captured frame for further processing

def release_video(cap):
    """
    Release the video stream and close all OpenCV windows.

    This function ensures that the camera is properly released and any OpenCV windows 
    are closed when the program finishes or an error occurs.
    """
    cap.release()  # Release the camera capture object
    cv2.destroyAllWindows()  # Close any OpenCV-created windows
