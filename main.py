from ui import PartCountingApp
import tkinter as tk

def main():
    """
    The main entry point for the Part Counting System.
    Initializes the UI and begins the program.
    """
    # Initialize the Tkinter root window
    root = tk.Tk()

    # Initialize the part counting application (UI and logic)
    app = PartCountingApp(root)

    # Start the Tkinter main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
