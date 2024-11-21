CONFIG = {
    # Camera settings
    'camera_index': 0,  # Camera index for OpenCV (0 for default, adjust for external camera)

    # Pre-processing settings
    'threshold_value': 128,  # Default threshold value for binary thresholding
    'low_canny_threshold': 50,  # Lower bound for Canny edge detection (adjust if needed)
    'high_canny_threshold': 150,  # Upper bound for Canny edge detection

    # UI settings (if needed in the future)
    'ui_update_interval': 100,  # Interval in milliseconds for updating the UI (can change to whatever rate you want)

    # Display settings... Can look up different colors if needed
    'contour_color': (0, 255, 0),  # Color for drawing contours (green)
    'count_color': (255, 0, 0),  # Color for displaying the part count (blue)
    'font_scale': 1,  # Font size for the part count display
    'font_thickness': 2,  # Font thickness for the part count display

    # Other settings (future-proofing)
    'blur_kernel_size': (5, 5),  # Kernel size for Gaussian blur
    'dilate_iterations': 1,  # Number of iterations for dilation
    'erode_iterations': 1,  # Number of iterations for erosion 
}
