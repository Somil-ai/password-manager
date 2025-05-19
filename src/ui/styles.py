import tkinter as tk
from tkinter import ttk
import platform

def apply_styles():
    """Apply custom styles to the application"""
    style = ttk.Style()
    
    # Define colors
    colors = {
        "bg_dark": "#0F172A",       # Sidebar background
        "bg_main": "#1E293B",       # Main background
        "text_primary": "#E2E8F0",  # Primary text
        "text_secondary": "#94A3B8",# Secondary text
        "accent": "#3B82F6",        # Accent color (blue)
        "accent_hover": "#2563EB",  # Accent hover
        "success": "#10B981",       # Success color (green)
        "warning": "#F59E0B",       # Warning color (amber)
        "error": "#EF4444",         # Error color (red)
        "border": "#334155",        # Border color
        "input_bg": "#1E293B",      # Input background
        "input_border": "#475569",  # Input border
    }
    
    # Configure TFrame styles
    style.configure("App.TFrame",
                   background=colors["bg_main"])
    style.configure("Sidebar.TFrame", background=colors["bg_dark"])
    
    # Configure Label styles
    style.configure("App.TLabel", 
                   background=colors["bg_main"],
                   foreground=colors["text_primary"])
    style.configure("Sidebar.TLabel", 
                   background=colors["bg_dark"],
                   foreground=colors["text_primary"])
    
    # Configure Button styles
    style.configure("App.TButton", 
                   background=colors["bg_main"],
                   foreground=colors["text_primary"],
                   borderwidth=1,
                   focusthickness=0,
                   focuscolor=colors["accent"])
    style.map("App.TButton",
             background=[("active", colors["bg_main"]), ("pressed", colors["bg_main"])],
             foreground=[("active", colors["accent"])])
    
    style.configure("Sidebar.TButton", 
                   background=colors["bg_dark"],
                   foreground=colors["text_primary"],
                   borderwidth=1,
                   focusthickness=0,
                   focuscolor=colors["accent"])
    style.map("Sidebar.TButton",
             background=[("active", colors["bg_dark"]), ("pressed", colors["bg_dark"])],
             foreground=[("active", colors["accent"])])
    
    style.configure("Accent.TButton", 
                   background=colors["accent"],
                   foreground="white",
                   borderwidth=0,
                   focusthickness=0)
    style.map("Accent.TButton",
             background=[("active", colors["accent_hover"]), ("pressed", colors["accent_hover"])])
    
    style.configure("Warning.TButton", 
                   background=colors["error"],
                   foreground="white",
                   borderwidth=0,
                   focusthickness=0)
    style.map("Warning.TButton",
             background=[("active", "#DC2626"), ("pressed", "#DC2626")])
    
    # Configure Entry styles
    style.configure("App.TEntry",
                   fieldbackground=colors["input_bg"],
                   foreground=colors["text_primary"],
                   bordercolor=colors["input_border"],
                   lightcolor=colors["input_border"],
                   darkcolor=colors["input_border"],
                   borderwidth=1,
                   padding=5)
    
    # Customize Entry selection colors
    # Note: This needs to be done with tk directly
    # style.map("App.TEntry",
    #         selectbackground=[("", colors["accent"])],
    #         selectforeground=[("", "white")])
    
    # Configure Password display entry
    style.configure("Password.TEntry",
                   fieldbackground=colors["bg_dark"],
                   foreground=colors["accent"],
                   bordercolor=colors["input_border"],
                   lightcolor=colors["input_border"],
                   darkcolor=colors["input_border"],
                   borderwidth=1,
                   padding=8,
                   font=("Courier", 14))
    
    # Configure Combobox
    style.configure("App.TCombobox",
                   fieldbackground=colors["input_bg"],
                   foreground=colors["text_primary"],
                   background=colors["input_bg"],
                   arrowcolor=colors["text_primary"])
    
    # Configure LabelFrame
    style.configure("App.TLabelframe", 
                   background=colors["bg_main"],
                   foreground=colors["text_primary"],
                   bordercolor=colors["border"],
                   borderwidth=1,
                   relief=tk.GROOVE)
    style.configure("App.TLabelframe.Label", 
                   background=colors["bg_main"],
                   foreground=colors["accent"])
    
    style.configure("Sidebar.TLabelframe", 
                   background=colors["bg_dark"],
                   foreground=colors["text_primary"],
                   bordercolor=colors["border"],
                   borderwidth=1,
                   relief=tk.GROOVE)
    style.configure("Sidebar.TLabelframe.Label", 
                   background=colors["bg_dark"],
                   foreground=colors["accent"])
    
    # Configure Checkbutton
    style.configure("App.TCheckbutton", 
                   background=colors["bg_main"],
                   foreground=colors["text_primary"],
                   indicatorcolor=colors["bg_main"],
                   indicatorrelief=tk.FLAT)
    style.map("App.TCheckbutton",
             background=[("active", colors["bg_main"])],
             indicatorcolor=[("selected", colors["accent"])])
    
    # Configure Radiobutton
    style.configure("Sidebar.TRadiobutton", 
                   background=colors["bg_dark"],
                   foreground=colors["text_primary"],
                   indicatorcolor=colors["bg_dark"],
                   indicatorrelief=tk.FLAT)
    style.map("Sidebar.TRadiobutton",
             background=[("active", colors["bg_dark"])],
             foreground=[("selected", colors["accent"])],
             indicatorcolor=[("selected", colors["accent"])])
    
    # Configure Treeview for password list
    style.configure("App.Treeview",
                   background=colors["bg_main"],
                   foreground=colors["text_primary"],
                   fieldbackground=colors["bg_main"],
                   bordercolor=colors["border"],
                   lightcolor=colors["border"],
                   darkcolor=colors["border"])
    style.map("App.Treeview",
             background=[("selected", colors["accent"])],
             foreground=[("selected", "white")])
    
    # Configure Treeview heading
    style.configure("App.Treeview.Heading",
                   background=colors["bg_dark"],
                   foreground=colors["text_primary"],
                   relief=tk.FLAT)
    style.map("App.Treeview.Heading",
             background=[("active", colors["bg_dark"])],
             foreground=[("active", colors["accent"])])
    
    # Configure scrollbars
    style.configure("TScrollbar",
                   troughcolor=colors["bg_main"],
                   background=colors["border"],
                   arrowcolor=colors["text_primary"])
    
    # Configure progressbar
    style.configure("TProgressbar",
                   troughcolor=colors["bg_dark"],
                   background=colors["accent"])
    
    # Set application colors
    if platform.system() == "Darwin":  # macOS
        # Special handling for macOS
        pass
    elif platform.system() == "Windows":
        # Special handling for Windows
        pass
    
    # Add new styles for vault creation frame
    style.configure("Vault.TFrame",
                   background=colors["bg_main"])
    
    style.configure("VaultTitle.TLabel",
                   font=("Arial", 24, "bold"),
                   foreground="#4B9EFF",  # Light blue color matching SecureVault text
                   background=colors["bg_main"])
    
    style.configure("VaultSubtitle.TLabel",
                   font=("Arial", 14),
                   foreground="#94A3B8",  # Light gray color
                   background=colors["bg_main"])
    
    style.configure("VaultField.TLabel",
                   font=("Arial", 12),
                   foreground=colors["text_primary"],
                   background=colors["bg_main"])
    
    style.configure("VaultEntry.TEntry",
                   fieldbackground=colors["input_bg"],
                   foreground=colors["text_primary"],
                   bordercolor=colors["input_border"],
                   borderwidth=1,
                   padding=8)
    
    return style