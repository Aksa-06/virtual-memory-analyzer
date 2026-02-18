import tkinter as tk

def create_main_window():
    root = tk.Tk()
    # Width x Height (in pixels)
    root.geometry("1200x750")
    root.minsize(1000, 600)  # Set minimum window size
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.configure(bg="#0f172a")  # dark theme background
    
    # Set window icon (using a simple colored square as placeholder)
    try:
        # Try to set a custom icon if available
        root.iconbitmap(default="icon.ico")
    except:
        # If no icon file exists, continue without icon
        pass
    
    return root
