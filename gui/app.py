import tkinter as tk
from tkinter import font as tkfont, ttk
from gui.layout import create_main_window
from backend.engine import simulate
from backend.detector import detect_thrashing
from gui.graphs import draw
import threading
import time
import pyttsx3

# Initialize text-to-speech engine
engine_instance = None

def speak(text):
    global engine_instance
    try:
        # Update subtitle immediately
        update_subtitle(text)
        
        # Create engine only when needed
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed of speech
        engine.setProperty('volume', 0.8)  # Volume level
        engine.say(text)
        engine.runAndWait()
        print(f"✓ Audio played: {text}")  # Debug confirmation
    except Exception as e:
        print(f"✗ TTS Error: {e}")  # Debug output
        # Try alternative method
        try:
            import winsound
            winsound.MessageBeep(1000, 200)  # Simple beep as fallback
            print("✓ Fallback beep played")
        except:
            print("✗ No audio available")


def run_simulation():
    try:
        frames = int(frame_entry.get())
        if frames <= 0:
            result_label.config(text="Please enter a positive number for frames!", fg="#ef4444")
            speak("Error: Please enter a positive number for memory frames.")
            return
    except ValueError:
        result_label.config(text="Please enter a valid number!", fg="#ef4444")
        speak("Error: Please enter a valid number for memory frames.")
        return
    
    try:
        min_load = int(min_entry.get())
        max_load = int(max_entry.get())
        step = int(step_entry.get())
        
        if min_load <= 0 or max_load <= 0 or step <= 0:
            result_label.config(text="Please enter positive numbers for process range!", fg="#ef4444")
            speak("Error: Please enter positive numbers for process range.")
            return
            
        if min_load > max_load:
            result_label.config(text="Minimum cannot be greater than maximum!", fg="#ef4444")
            speak("Error: Minimum process load cannot be greater than maximum.")
            return
            
        if step > (max_load - min_load):
            result_label.config(text="Step size too large for range!", fg="#ef4444")
            speak("Error: Step size is too large for the specified range.")
            return
            
    except ValueError:
        result_label.config(text="Please enter valid numbers for process range!", fg="#ef4444")
        speak("Error: Please enter valid numbers for process range configuration.")
        return
    
    # Show loading state
    run_button.config(text="Running...", state="disabled", bg="#6b7280")
    root.update()
    
    speak(f"Starting simulation with {frames} memory frames, testing processes from {min_load} to {max_load} with step size {step}.")
    
    loads = list(range(min_load, max_load + 1, step))
    accesses = 500

    faults = []
    cpu = []

    for l in loads:
        pf = simulate(l, frames)
        faults.append(pf)
        cpu_util = 100 * (1 - (pf / accesses))
        cpu.append(cpu_util)

    t = detect_thrashing(loads, faults, cpu)

    if t and t > 0:
        result_label.config(text=f"✨ Thrashing starts at load: {t}", fg="#10b981")
        explanation = f"Thrashing detected at system load {t}. This means when there are {t} or more processes, the system spends more time managing memory than doing actual work. Consider increasing memory frames or reducing the number of concurrent processes."
        speak(explanation)
    else:
        result_label.config(text="✅ No thrashing detected within tested range", fg="#10b981")
        explanation = f"Good news! No thrashing detected with {frames} memory frames across all tested system loads from {min_load} to {max_load} with step size {step}. Your system configuration is well-balanced for the tested workload."
        speak(explanation)
    
    # Reset button
    run_button.config(text="Run Simulation", state="normal", bg="#8b5cf6")
    
    draw(loads, faults, cpu, t)


root = create_main_window()
root.title("🚀 Virtual Memory Performance Analyzer")

# Define modern, colorful fonts
title_font = tkfont.Font(family="Segoe UI", size=16, weight="bold")
subtitle_font = tkfont.Font(family="Segoe UI", size=12, weight="normal")
body_font = tkfont.Font(family="Segoe UI", size=11)
button_font = tkfont.Font(family="Segoe UI", size=12, weight="bold")

# Create main container with padding
main_frame = tk.Frame(root, bg="#0f172a")
main_frame.pack(expand=True, fill="both", padx=40, pady=30)

# Title section
title_frame = tk.Frame(main_frame, bg="#0f172a")
title_frame.pack(pady=(0, 30))

tk.Label(
    title_frame,
    text="🎯 Virtual Memory Performance Analyzer",
    font=title_font,
    fg="#fbbf24",
    bg="#0f172a",
).pack()

tk.Label(
    title_frame,
    text="Analyze system performance and detects thrashing patterns",
    font=subtitle_font,
    fg="#94a3b8",
    bg="#0f172a",
).pack(pady=(5, 0))

# Input section
input_frame = tk.Frame(main_frame, bg="#1e293b", relief="raised", bd=1)
input_frame.pack(fill="x", pady=(0, 20), ipady=20, ipadx=20)

# Memory Frames Input
tk.Label(
    input_frame,
    text="💾 Physical Memory Frames:",
    font=body_font,
    fg="#e2e8f0",
    bg="#1e293b",
).pack(pady=(0, 8))

# Styled entry with frame
entry_frame = tk.Frame(input_frame, bg="#334155", relief="solid", bd=1)
entry_frame.pack(pady=(0, 15))

frame_entry = tk.Entry(
    entry_frame, 
    font=body_font, 
    bg="#334155", 
    fg="#f1f5f9",
    insertbackground="#f1f5f9",
    relief="flat",
    bd=8,
    width=15,
    selectbackground="#8b5cf6",
    selectforeground="#ffffff"
)
frame_entry.insert(0, "30")
frame_entry.pack(padx=2, pady=2)

# Add entry focus effects
def on_entry_focus_in(e):
    entry_frame.config(bg="#4c1d95", relief="solid", bd=2)
    frame_entry.config(bg="#4c1d95")

def on_entry_focus_out(e):
    entry_frame.config(bg="#334155", relief="solid", bd=1)
    frame_entry.config(bg="#334155")

frame_entry.bind("<FocusIn>", on_entry_focus_in)
frame_entry.bind("<FocusOut>", on_entry_focus_out)

# Process Range Configuration
process_frame = tk.Frame(input_frame, bg="#1e293b")
process_frame.pack(pady=(10, 0), fill="x")

tk.Label(
    process_frame,
    text="⚙️ Process Load Configuration:",
    font=body_font,
    fg="#fbbf24",
    bg="#1e293b",
).pack(pady=(0, 10))

# Process range inputs container
range_container = tk.Frame(process_frame, bg="#1e293b")
range_container.pack()

# Minimum processes
min_frame = tk.Frame(range_container, bg="#1e293b")
min_frame.pack(side="left", padx=10)
tk.Label(min_frame, text="Min:", font=body_font, fg="#e2e8f0", bg="#1e293b").pack()
min_entry = tk.Entry(min_frame, font=body_font, bg="#334155", fg="#f1f5f9", width=8)
min_entry.insert(0, "1")
min_entry.pack()

# Maximum processes
max_frame = tk.Frame(range_container, bg="#1e293b")
max_frame.pack(side="left", padx=10)
tk.Label(max_frame, text="Max:", font=body_font, fg="#e2e8f0", bg="#1e293b").pack()
max_entry = tk.Entry(max_frame, font=body_font, bg="#334155", fg="#f1f5f9", width=8)
max_entry.insert(0, "30")
max_entry.pack()

# Step size
step_frame = tk.Frame(range_container, bg="#1e293b")
step_frame.pack(side="left", padx=10)
tk.Label(step_frame, text="Step:", font=body_font, fg="#e2e8f0", bg="#1e293b").pack()
step_entry = tk.Entry(step_frame, font=body_font, bg="#334155", fg="#f1f5f9", width=8)
step_entry.insert(0, "1")
step_entry.pack()

# Add hint label
tk.Label(
    input_frame,
    text="💡 Configure process range and step size for detailed analysis",
    font=subtitle_font,
    fg="#64748b",
    bg="#1e293b",
).pack(pady=(10, 0))

# Button section
def on_enter(e):
    run_button.config(bg="#7c3aed", fg="#ffffff")

def on_leave(e):
    if run_button['state'] != 'disabled':
        run_button.config(bg="#8b5cf6", fg="#ffffff")

run_button = tk.Button(
    main_frame,
    text="🚀 Run Simulation",
    command=run_simulation,
    font=button_font,
    bg="#8b5cf6",  # purple
    fg="#ffffff",
    activebackground="#7c3aed",
    activeforeground="#ffffff",
    relief="flat",
    bd=0,
    padx=30,
    pady=12,
    cursor="hand2"
)
run_button.pack(pady=15)

# Bind hover events
run_button.bind("<Enter>", on_enter)
run_button.bind("<Leave>", on_leave)

# Result section
result_frame = tk.Frame(main_frame, bg="#1e293b", relief="solid", bd=1)
result_frame.pack(fill="x", ipady=15, ipadx=20)

result_label = tk.Label(
    result_frame, 
    text="📊 Ready to analyze performance...", 
    font=body_font, 
    fg="#94a3b8", 
    bg="#1e293b"
)
result_label.pack()

# Subtitle display for audio
subtitle_frame = tk.Frame(main_frame, bg="#0f172a", relief="solid", bd=1)
subtitle_frame.pack(fill="x", pady=(10, 0), ipady=10, ipadx=20)

subtitle_label = tk.Label(
    subtitle_frame,
    text="",
    font=subtitle_font,
    fg="#fbbf24",
    bg="#0f172a",
    wraplength=1000,
    justify="center"
)
subtitle_label.pack()

def update_subtitle(text):
    """Update subtitle with current audio text"""
    subtitle_label.config(text=f"🔊 {text}")
    # Auto-clear subtitle after 8 seconds
    root.after(8000, lambda: subtitle_label.config(text=""))

# Footer info
footer_frame = tk.Frame(main_frame, bg="#0f172a")
footer_frame.pack(side="bottom", pady=(20, 0))

tk.Label(
    footer_frame,
    text="⚡ Optimized for systems with 1-30 processes",
    font=subtitle_font,
    fg="#475569",
    bg="#0f172a",
).pack()

# Add window close handler
def on_closing():
    """Clean shutdown when main window is closed"""
    try:
        # Stop any running TTS
        global engine_instance
        if engine_instance is not None:
            engine_instance.stop()
    except:
        pass
    
    # Close any open graph windows
    try:
        # Import fig_window from graphs module
        import gui.graphs as graphs_module
        if hasattr(graphs_module, 'fig_window') and graphs_module.fig_window is not None:
            graphs_module.fig_window.destroy()
    except:
        pass
    
    # Terminate the application
    root.destroy()
    root.quit()

# Bind the close event
root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()
