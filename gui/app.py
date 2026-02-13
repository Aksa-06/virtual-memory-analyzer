import tkinter as tk
from tkinter import font as tkfont
from gui.layout import create_main_window
from backend.engine import simulate
from backend.detector import detect_thrashing
from gui.graphs import draw
from gui.audio import speak

def run_simulation():
    loads = list(range(1, 30))
    frames = int(frame_entry.get())

    faults = []
    cpu = []

    speak("Simulation started. Demand paging enabled.")

    for l in loads:
        pf = simulate(l, frames)
        faults.append(pf)
        cpu.append(max(0, 100 - pf*0.05))

    t = detect_thrashing(loads, faults)

    speak("Thrashing detected. CPU utilization collapsing.")
    speak(f"Thrashing starts at load {t}")

    result_label.config(text=f"Thrashing starts at load: {t}")

    draw(loads, faults, cpu)

root = create_main_window()
root.title("Virtual Memory Performance Analyzer")

# Define nicer, larger fonts
title_font = tkfont.Font(family="Segoe UI", size=14, weight="bold")
body_font = tkfont.Font(family="Segoe UI", size=12)

tk.Label(
    root,
    text="Frames (Physical Memory):",
    font=title_font,
    fg="#e5e7eb",
    bg="#0f172a",
).pack(pady=(10, 4))

frame_entry = tk.Entry(root, font=body_font)
frame_entry.insert(0, "30")
frame_entry.pack(pady=(0, 8))

tk.Button(
    root,
    text="Run Simulation",
    command=run_simulation,
    font=body_font,
    bg="#22c55e",          # emerald green
    fg="#022c22",
    activebackground="#16a34a",
    activeforeground="#f9fafb",
    relief="raised",
).pack(pady=10)

result_label = tk.Label(root, text="", font=body_font, fg="#f9fafb", bg="#0f172a")
result_label.pack(pady=(10, 0))

root.mainloop()
