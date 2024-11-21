import cv2
import json
import os


# Path to store the part database in JSON format
DATABASE_FILE = 'part_database.json'

def load_part_database():
    """Load the part database from the JSON file."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    else:
        return {}

def save_part_database(database):
    """Save the part database to the JSON file."""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(database, f, indent=4)

def scan_new_part(frame):
    """
    Scan a new part and determine its size (min_area and max_area).

    Returns:
    - min_area: Minimum contour area for the part.
    - max_area: Maximum contour area for the part.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour, assuming it's the part
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        # Set min and max area for future detection with a 10% margin
        min_area = int(area * 0.9)
        max_area = int(area * 1.1)
        return min_area, max_area
    else:
        print("No contours detected for the part.")
        return None, None


    """
    Add a new part to the part database.

    Parameters:
    - part_name: Name of the part.
    - part_id: Unique ID for the part.
    - company_name: Name of the company using the part.
    - min_area: Minimum contour area for the part.
    - max_area: Maximum contour area for the part.
    """
    database = load_part_database()

    # Add the new part data to the database
    database[part_id] = {
        'part_name': part_name,
        'company_name': company_name,
        'min_area': min_area,
        'max_area': max_area
    }

    # Save the updated database back to the JSON file
    save_part_database(database)

def scan_and_save_part(frame):
    """
    Scan a part and prompt the user for input to save the part in the database.

    Parameters:
    - frame: The current frame containing the part to scan.
    """
    min_area, max_area = scan_new_part(frame)

    if min_area and max_area:
        # Prompt user for part details
        part_name = input("Enter the part name: ")
        part_id = input("Enter the part ID: ")
        company_name = input("Enter the company name: ")

        # Add the new part to the database
        add_part_to_database(part_name, part_id, company_name, min_area, max_area)
        print(f"Part '{part_name}' saved to the database.")
    else:
        print("Failed to scan the part. Please try again.")
