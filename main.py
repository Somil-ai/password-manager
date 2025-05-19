import tkinter as tk
from tkinter import ttk
import sys
from src.ui.app import PasswordManagerApp

def main():
    """Main entry point for the application."""
    root = tk.Tk()
    root.title("SecureVault - Password Manager")
    root.minsize(900, 600)
    
    # Set the application icon
    try:
        # This would be replaced with your actual icon
        root.iconbitmap("assets/icon.ico")
    except:
        pass
    
    app = PasswordManagerApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    # Center the window on the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 1000
    window_height = 700
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()