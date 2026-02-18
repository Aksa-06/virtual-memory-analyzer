import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import rcParams
import tkinter as tk

# Set modern style and colors
plt.style.use('dark_background')
rcParams['figure.facecolor'] = '#1e293b'
rcParams['axes.facecolor'] = '#0f172a'
rcParams['axes.edgecolor'] = '#475569'
rcParams['axes.labelcolor'] = '#e2e8f0'
rcParams['xtick.color'] = '#94a3b8'
rcParams['ytick.color'] = '#94a3b8'
rcParams['text.color'] = '#e2e8f0'
rcParams['font.family'] = 'DejaVu Sans'

# Disable interactive navigation (zoom, pan)
plt.rcParams['toolbar'] = 'None'

import os
from datetime import datetime

# Global variable to store the figure window
fig_window = None

# Create graphs directory if it doesn't exist
GRAPHS_DIR = "performance_graphs"
if not os.path.exists(GRAPHS_DIR):
    os.makedirs(GRAPHS_DIR)

def draw(loads, faults, cpu, t=None):
    global fig_window
    
    # Close previous figure window if exists
    if fig_window is not None:
        try:
            plt.close(fig_window)
        except:
            pass
    
    fig = plt.figure(figsize=(14, 6), facecolor='#1e293b')
    
    # Create custom colors
    page_fault_color = '#ef4444'  # red
    cpu_color = '#3b82f6'  # blue
    thrashing_color = '#fbbf24'  # amber
    grid_color = '#334155'
    
    # Page Faults subplot
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(loads, faults, marker='o', color=page_fault_color, 
             linewidth=3, markersize=8, markerfacecolor=page_fault_color,
             markeredgecolor='#ffffff', markeredgewidth=1.5, label='Page Faults')
    ax1.fill_between(loads, faults, alpha=0.3, color=page_fault_color)
    ax1.set_title("Page Faults Analysis", fontsize=14, fontweight='bold', color='#fbbf24', pad=20)
    ax1.set_xlabel("System Load (Processes)", fontsize=12, color='#e2e8f0')
    ax1.set_ylabel("Page Fault Count", fontsize=12, color='#e2e8f0')
    ax1.grid(True, alpha=0.2, color=grid_color, linestyle='--')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color(grid_color)
    ax1.spines['bottom'].set_color(grid_color)
    
    if t:
        ax1.axvline(x=t, linestyle='--', color=thrashing_color, linewidth=2.5, 
                   alpha=0.8, label=f'Thrashing Point (Load: {t})')
        ax1.legend(loc='upper left', frameon=True, fancybox=True, shadow=True,
                   facecolor='#1e293b', edgecolor='#475569', labelcolor='#e2e8f0')
    
    # CPU Utilization subplot
    ax2 = plt.subplot(1, 2, 2)
    ax2.plot(loads, cpu, marker='s', color=cpu_color, 
             linewidth=3, markersize=8, markerfacecolor=cpu_color,
             markeredgecolor='#ffffff', markeredgewidth=1.5, label='CPU Utilization')
    ax2.fill_between(loads, cpu, alpha=0.3, color=cpu_color)
    ax2.set_title("CPU Utilization Analysis", fontsize=14, fontweight='bold', color='#fbbf24', pad=20)
    ax2.set_xlabel("System Load (Processes)", fontsize=12, color='#e2e8f0')
    ax2.set_ylabel("CPU Utilization (%)", fontsize=12, color='#e2e8f0')
    ax2.grid(True, alpha=0.2, color=grid_color, linestyle='--')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color(grid_color)
    ax2.spines['bottom'].set_color(grid_color)
    ax2.set_ylim(0, 105)  # Set y-axis limit to 100%
    
    if t:
        ax2.axvline(x=t, linestyle='--', color=thrashing_color, linewidth=2.5, 
                   alpha=0.8, label=f'Thrashing Point (Load: {t})')
        ax2.legend(loc='upper left', frameon=True, fancybox=True, shadow=True,
                   facecolor='#1e293b', edgecolor='#475569', labelcolor='#e2e8f0')
    
    # Add main title
    fig.suptitle('Virtual Memory Performance Analysis', fontsize=16, fontweight='bold', 
                color='#fbbf24', y=0.98)
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.88)  # Adjust for suptitle
    
    # Create a new window for the graph with custom toolbar
    graph_window = tk.Toplevel()
    graph_window.title("Performance Analysis Graph")
    graph_window.geometry("1450x750")
    graph_window.configure(bg='#1e293b')
    
    # Embed matplotlib figure in tkinter window
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1, padx=10, pady=10)
    
    # Create a custom toolbar frame
    toolbar_frame = tk.Frame(graph_window, bg='#1e293b', height=60)
    toolbar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
    
    # Add custom buttons
    def save_graph():
        from tkinter import messagebox
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"performance_analysis_{timestamp}.png"
        file_path = os.path.join(GRAPHS_DIR, filename)
        
        fig.savefig(file_path, dpi=300, bbox_inches='tight', facecolor='#1e293b')
        messagebox.showinfo("Success", f"Graph saved to {file_path}")
        
        # Audio explanation for save
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            
            def speak_save():
                engine.say(f"Performance graph saved successfully to {GRAPHS_DIR} folder with filename {filename}.")
                engine.runAndWait()
            
            threading.Thread(target=speak_save, daemon=True).start()
        except:
            pass
    
    def close_graph():
        global fig_window
        graph_window.destroy()
        fig_window = None
    
    # Style for buttons
    button_style = {
        'bg': '#8b5cf6',
        'fg': '#ffffff',
        'font': ('DejaVu Sans', 10, 'bold'),
        'relief': 'flat',
        'bd': 0,
        'padx': 15,
        'pady': 5,
        'cursor': 'hand2',
        'activebackground': '#7c3aed',
        'activeforeground': '#ffffff'
    }
    
    # Create buttons
    tk.Label(toolbar_frame, text="Graph Controls:", bg='#1e293b', fg='#fbbf24', 
            font=('DejaVu Sans', 11, 'bold')).pack(side=tk.LEFT, padx=10)
    
    tk.Button(toolbar_frame, text="Save", command=save_graph, **button_style).pack(side=tk.LEFT, padx=5)
    tk.Button(toolbar_frame, text="Close", command=close_graph, **button_style).pack(side=tk.LEFT, padx=5)
    
    # Add hover effects
    def on_button_enter(e, btn):
        btn.config(bg='#7c3aed')
    
    def on_button_leave(e, btn):
        btn.config(bg='#8b5cf6')
    
    # Apply hover effects to all buttons
    for widget in toolbar_frame.winfo_children():
        if isinstance(widget, tk.Button):
            widget.bind("<Enter>", lambda e, btn=widget: on_button_enter(e, btn))
            widget.bind("<Leave>", lambda e, btn=widget: on_button_leave(e, btn))
    
    # Store reference to figure window
    fig_window = graph_window
