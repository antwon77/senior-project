import cv2

# Example part database with min and max areas for each part type
part_database = {
    'Part1': {'min_area': 500, 'max_area': 1000},
    'Part2': {'min_area': 1200, 'max_area': 1800},
    # Additional parts can be added here
}

def get_part_size_filters(part_name):
    """Retrieve the min_area and max_area for the selected part from the database."""
    part_info = part_database.get(part_name)
    if part_info:
        return part_info['min_area'], part_info['max_area']
    else:
        print(f"Error: Part {part_name} not found in database.")
        return None, None

def detect_contours(image, min_area, max_area):
    """
    Detect contours and filter them based on dynamic size filters.

    Parameters:
    - image: Pre-processed binary or edge-detected image.
    - min_area: Minimum contour area to be considered a valid part (retrieved dynamically).
    - max_area: Maximum contour area to be considered a valid part (retrieved dynamically).

    Returns:
    - valid_contours: List of valid contours that meet the size criteria.
    """
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on dynamically retrieved area (size)
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            valid_contours.append(contour)  # Add valid contours to the list

    return valid_contours

def count_parts(contours):
    """Count the number of valid parts (contours)."""
    return len(contours)

def draw_contours(image, contours):
    """Draw contours on the image for visualization."""
    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    return image

def add_count_to_image(image, count):
    """Display the current part count on the image in real-time."""
    cv2.putText(image, f"Count: {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return image
