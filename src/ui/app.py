import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
from src.ui.login_frame import LoginFrame
from src.ui.dashboard import DashboardFrame
from src.ui.styles import apply_styles

class PasswordManagerApp(ttk.Frame):
    """Main application class for the password manager"""
    
    def __init__(self, master):
        """Initialize the password manager application"""
        super().__init__(master)
        self.master = master
        
        # Apply custom styles
        self.style = apply_styles()
        
        # Initialize variables
        self.current_frame = None
        self.authenticated = False
        self.encryption_handler = None
        self.password_store = None
        self.inactivity_timer = None
        self.auto_lock_time = 5 * 60  # 5 minutes
        
        # Start with login screen
        self._show_login()
        
        # Set up event bindings
        self.master.bind("<Button-1>", self._reset_inactivity_timer)
        self.master.bind("<Key>", self._reset_inactivity_timer)
        
    def _show_login(self):
        """Show the login frame"""
        if self.current_frame:
            self.current_frame.destroy()
        
        self.login_frame = LoginFrame(self, self.on_login_success)
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.login_frame
    
    def _show_dashboard(self):
        """Show the dashboard frame"""
        if self.current_frame:
            self.current_frame.destroy()
            
        self.dashboard = DashboardFrame(
            self, 
            self.encryption_handler, 
            self.password_store, 
            self.on_logout
        )
        self.dashboard.pack(fill=tk.BOTH, expand=True)
        self.current_frame = self.dashboard
        
    def on_login_success(self, encryption_handler, password_store):
        """Handle successful login"""
        self.authenticated = True
        self.encryption_handler = encryption_handler
        self.password_store = password_store
        self._show_dashboard()
        self._reset_inactivity_timer()
    
    def on_logout(self):
        """Handle logout"""
        self.authenticated = False
        self.encryption_handler = None
        self.password_store = None
        if self.inactivity_timer:
            self.inactivity_timer.cancel()
            self.inactivity_timer = None
        self._show_login()
        
    def _reset_inactivity_timer(self, event=None):
        """Reset the inactivity timer"""
        if self.authenticated:
            if self.inactivity_timer:
                self.inactivity_timer.cancel()
            
            self.inactivity_timer = threading.Timer(self.auto_lock_time, self._auto_lock)
            self.inactivity_timer.daemon = True
            self.inactivity_timer.start()
    
    def _auto_lock(self):
        """Automatically lock the application after inactivity"""
        if self.authenticated:
            messagebox.showinfo("Auto-Lock", "Application locked due to inactivity")
            self.on_logout()