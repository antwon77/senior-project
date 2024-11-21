import cv2
import tkinter as tk
from tkinter import messagebox

def show_alert():
    """Create a UI alert when the video feed drops."""
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Camera Error", "The video feed has been lost. Please check the connection.")
    root.destroy()

def capture_video(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        show_alert()
        return None
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cap.set(cv2.CAP_PROP_FPS, 60)
    return cap

def read_frame(cap):
    ret, frame = cap.read()
    if not ret:
        show_alert()
        release_video(cap)
        exit()
    return frame

def release_video(cap):
    cap.release()
    cv2.destroyAllWindows()
