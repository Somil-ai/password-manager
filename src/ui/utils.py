import tkinter as tk
from tkinter import ttk

def center_window(window):
    """Center a window on the screen"""
    window.update_idletasks()
    
    width = window.winfo_width()
    height = window.winfo_height()
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_tooltip(widget, text):
    """Create a tooltip for a widget"""
    try:
        from tkinter_tooltip import ToolTip
        ToolTip(widget, text)
    except ImportError:
        def on_enter(event):
            x = y = 0
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 20

            # Create a toplevel window
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            
            label = ttk.Label(
                tooltip, 
                text=text, 
                justify=tk.LEFT,
                background="#0F172A",
                foreground="#E2E8F0",
                relief=tk.SOLID,
                borderwidth=1,
                padx=5,
                pady=2
            )
            label.pack(ipadx=1)
            
            widget.tooltip = tooltip

        def on_leave(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)