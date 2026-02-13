import tkinter as tk

def create_main_window():
    root = tk.Tk()
    root.title("Virtual Memory Performance Analyzer")

    # Medium-sized window instead of fullscreen
    # Width x Height (in pixels)
    root.geometry("1100x700")

    root.configure(bg="#0f172a")  # dark theme background

    return root
