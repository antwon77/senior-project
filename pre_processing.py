import cv2
import numpy as np

def preprocess_image(image):
    """Pre-process the image by converting to grayscale and applying Gaussian blur."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply Gaussian blur to reduce noise
    return blurred

def apply_clahe(image):
    """Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to improve contrast."""
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized = clahe.apply(image)
    return equalized

def apply_threshold(image, threshold_value=128, use_otsu=False):
    """Apply binary or Otsu's thresholding to the image."""
    if use_otsu:
        _, thresh_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    else:
        _, thresh_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresh_image

def apply_bilateral_filter(image, d=9, sigmaColor=75, sigmaSpace=75):
    """Apply bilateral filtering to reduce noise while preserving edges."""
    filtered_image = cv2.bilateralFilter(image, d, sigmaColor, sigmaSpace)
    return filtered_image

def apply_canny_edge_detection(image, low_threshold=50, high_threshold=150):
    """Apply Canny edge detection to detect the edges of thin objects."""
    edges = cv2.Canny(image, low_threshold, high_threshold)
    return edges

def apply_morphological_operations(image, dilate_iterations=1, erode_iterations=1):
    """Apply morphological operations to strengthen or clean up edges."""
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    dilated = cv2.dilate(image, kernel, iterations=dilate_iterations)
    eroded = cv2.erode(dilated, kernel, iterations=erode_iterations)
    return eroded

def adaptive_morphological_operations(image, object_size):
    """Adapt kernel size dynamically based on object size for dilation/erosion."""
    kernel_size = max(3, int(object_size / 50))  # Adjust kernel size dynamically
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    dilated = cv2.dilate(image, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)
    return eroded

def remove_shadows(image):
    """Apply shadow removal techniques to improve part visibility."""
    dilated_img = cv2.dilate(image, np.ones((7,7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(image, bg_img)
    norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    return norm_img
