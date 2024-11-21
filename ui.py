import tkinter as tk
from tkinter import ttk, messagebox
import json
import cv2
from .part_scanner import scan_and_save_part, load_part_database
from .contour_detection import detect_contours, count_parts, draw_contours, add_count_to_image
from .pre_processing import preprocess_image, apply_canny_edge_detection
from .config import CONFIG
from .capture import capture_video, read_frame, release_video


class PartCountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Part Counting System")
        self.selected_part_id = tk.StringVar()

        # Load the part database
        self.part_database = load_part_database()

        # Create the dropdown menu for part selection
        self.create_part_selection_ui()

        # Create the form to scan and save new parts
        self.create_scan_part_ui()

        # Button to start the counting option screen
        self.start_count_option_button = tk.Button(self.root, text="Start Counting", command=self.show_count_options)
        self.start_count_option_button.pack(pady=10)

        # Real-time count display
        self.count_label = tk.Label(self.root, text="Part Count: 0", font=("Arial", 16))
        self.count_label.pack(pady=20)

    def create_part_selection_ui(self):
        """Create a dropdown menu for part selection from the database."""
        tk.Label(self.root, text="Select Part to Count:", font=("Arial", 12)).pack(pady=10)
        part_options = list(self.part_database.keys())  # List of part IDs

        # Dropdown menu
        self.part_dropdown = ttk.Combobox(self.root, textvariable=self.selected_part_id, values=part_options)
        self.part_dropdown.pack(pady=10)
        self.part_dropdown.set(part_options[0] if part_options else "")

    def create_scan_part_ui(self):
        """Create a form to scan and save new parts into the database."""
        tk.Label(self.root, text="Scan and Save a New Part", font=("Arial", 12)).pack(pady=10)

        # Input fields for part name, part ID, and company name
        self.part_name_entry = tk.Entry(self.root, width=30)
        self.part_name_entry.insert(0, "Part Name")
        self.part_name_entry.pack(pady=5)

        self.part_id_entry = tk.Entry(self.root, width=30)
        self.part_id_entry.insert(0, "Part ID")
        self.part_id_entry.pack(pady=5)

        self.company_name_entry = tk.Entry(self.root, width=30)
        self.company_name_entry.insert(0, "Company Name")
        self.company_name_entry.pack(pady=5)

        # Button to scan and save the new part
        save_part_button = tk.Button(self.root, text="Scan and Save Part", command=self.scan_and_save_part)
        save_part_button.pack(pady=10)

    def scan_and_save_part(self):
        """Scan the new part and save it into the database."""
        part_name = self.part_name_entry.get()
        part_id = self.part_id_entry.get()
        company_name = self.company_name_entry.get()

        if part_name and part_id and company_name:
            cap = capture_video(CONFIG['camera_index'])  # Capture the video feed
            frame = read_frame(cap)  # Read a single frame for scanning the part

            # Scan the part and save it in the database
            scan_and_save_part(frame)
            release_video(cap)  # Release the video capture

            # Update part dropdown after saving
            self.part_database = load_part_database()
            self.part_dropdown['values'] = list(self.part_database.keys())

            messagebox.showinfo("Success", f"Part '{part_name}' has been saved!")
        else:
            messagebox.showwarning("Input Error", "Please fill out all fields before saving.")

    def show_count_options(self):
        """Show options for continuous counting or counting to a specific number."""
        self.count_option_window = tk.Toplevel(self.root)
        self.count_option_window.title("Counting Options")

        tk.Label(self.count_option_window, text="Choose Counting Mode:", font=("Arial", 12)).pack(pady=10)

        # Button for continuous counting
        continuous_button = tk.Button(self.count_option_window, text="Count Continuously", command=self.start_continuous_counting)
        continuous_button.pack(pady=5)

        # Entry and button for counting to a specific number
        tk.Label(self.count_option_window, text="Or enter a target count:", font=("Arial", 12)).pack(pady=10)

        self.target_count_entry = tk.Entry(self.count_option_window, width=10)
        self.target_count_entry.pack(pady=5)

        target_button = tk.Button(self.count_option_window, text="Start Counting to Target", command=self.start_target_counting)
        target_button.pack(pady=5)

    def start_continuous_counting(self):
        """Start counting parts continuously until no more parts are detected for a set amount of space."""
        self.count_option_window.destroy()  # Close the option window
        self.start_counting()

    def start_target_counting(self):
        """Start counting parts until the target count is reached."""
        try:
            target_count = int(self.target_count_entry.get())
            self.count_option_window.destroy()  # Close the option window
            self.start_counting(target_count)
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter a valid number for the target count.")

    def start_counting(self, target_count=None):
        """Start real-time part counting based on the selected part, with an optional target count."""
        part_id = self.selected_part_id.get()

        if part_id not in self.part_database:
            messagebox.showwarning("Part Selection Error", "Please select a valid part to count.")
            return

        # Retrieve size filters from the database for the selected part
        part_info = self.part_database[part_id]
        min_area = part_info['min_area']
        max_area = part_info['max_area']

        # Start video capture for counting
        cap = capture_video(CONFIG['camera_index'])
        current_count = 0
        empty_frames_count = 0  # Track how many consecutive frames had no part detected
        max_empty_frames = 50  # <-- This is where you can adjust the number of frames considered "space" without parts

        while True:
            frame = read_frame(cap)
            if frame is None:
                break

            # Pre-process the frame and apply Canny edge detection
            processed_frame = preprocess_image(frame)
            edges = apply_canny_edge_detection(processed_frame)

            # Detect contours based on the part's size
            contours = detect_contours(edges, min_area, max_area)

            # Count the parts
            part_count = count_parts(contours)
            if part_count == 0:
                empty_frames_count += 1
            else:
                current_count += part_count
                empty_frames_count = 0  # Reset the empty frame count when a part is detected

            self.count_label.config(text=f"Part Count: {current_count}")

            # Draw contours on the frame
            frame_with_contours = draw_contours(frame, contours)

            # Display the frame with real-time updates
            cv2.imshow('Part Counting System', frame_with_contours)

            # Stop if we've gone through the max number of empty frames without detecting parts
            if empty_frames_count > max_empty_frames:
                messagebox.showinfo("Stopped", "Counting stopped due to no part detection for a set amount of space.")
                break

            # If target count is set and reached, stop the program
            if target_count and current_count >= target_count:
                messagebox.showinfo("Target Reached", f"Target of {target_count} parts reached!")
                break

            # Exit on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video stream and close OpenCV windows
        release_video(cap)
        cv2.destroyAllWindows()

        # After the target count is reached or counting is stopped, pause further counting
        # Optionally, disable counting buttons here to prevent continuing until reset
        self.start_count_option_button.config(state=tk.NORMAL)
        messagebox.showinfo("Counting Paused", "Counting paused. You can restart or begin a new count.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PartCountingApp(root)
    root.mainloop()
