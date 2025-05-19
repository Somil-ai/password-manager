import tkinter as tk
from tkinter import ttk, messagebox
import os
from src.core.encryption import PasswordEncryption
from src.core.password_store import PasswordStore
from src.ui.utils import center_window

class LoginFrame(ttk.Frame):  # Change from tk.Frame to ttk.Frame
    """Frame for handling user login and master password"""
    
    def __init__(self, parent, on_login_callback):
        """Initialize the login frame"""
        super().__init__(parent, style="App.TFrame")  # Now this will work with ttk
        self.parent = parent
        self.on_login_callback = on_login_callback
        self.salt_exists = self._check_salt_exists()
        
        self._create_widgets()
    
    def _check_salt_exists(self):
        """Check if a salt file exists (indicates first-time setup)"""
        salt_file = os.path.join(os.path.expanduser("~"), ".securevault", "salt")
        return os.path.exists(salt_file)
    
    def _create_widgets(self):
        """Create the login UI widgets"""
        # Main container with padding
        container = ttk.Frame(self, style="App.TFrame")
        container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # App logo/header
        logo_frame = ttk.Frame(container, style="App.TFrame")
        logo_frame.pack(pady=(0, 30))
        
        logo_label = ttk.Label(
            logo_frame, 
            text="SecureVault", 
            font=("Helvetica", 28, "bold"),
            foreground="#3B82F6",
            background="#1E293B"
        )
        logo_label.pack()
        
        tagline = ttk.Label(
            logo_frame,
            text="Password Manager & Generator",
            font=("Helvetica", 14),
            foreground="#94A3B8",
            background="#1E293B"
        )
        tagline.pack(pady=(5, 0))
        
        # Login form
        form_frame = ttk.Frame(container, style="App.TFrame")
        form_frame.pack(pady=10)
        
        # Title based on whether this is first time or not
        title_text = "Create Master Password" if not self.salt_exists else "Enter Master Password"
        title = ttk.Label(
            form_frame,
            text=title_text,
            font=("Helvetica", 16, "bold"),
            foreground="#E2E8F0",
            background="#1E293B"
        )
        title.pack(pady=(0, 20))
        
        # Password entry
        password_frame = ttk.Frame(form_frame, style="App.TFrame")
        password_frame.pack(fill=tk.X, pady=5)
        
        password_label = ttk.Label(
            password_frame,
            text="Master Password:",
            font=("Helvetica", 12),
            foreground="#E2E8F0",
            background="#1E293B"
        )
        password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            show="●",
            width=30,
            style="App.TEntry"
        )
        self.password_entry.pack(fill=tk.X)
        
        # Confirm password field (only for first-time setup)
        if not self.salt_exists:
            confirm_frame = ttk.Frame(form_frame, style="App.TFrame")
            confirm_frame.pack(fill=tk.X, pady=10)
            
            confirm_label = ttk.Label(
                confirm_frame,
                text="Confirm Password:",
                font=("Helvetica", 12),
                foreground="#E2E8F0",
                background="#1E293B"
            )
            confirm_label.pack(anchor=tk.W, pady=(0, 5))
            
            self.confirm_var = tk.StringVar()
            self.confirm_entry = ttk.Entry(
                confirm_frame,
                textvariable=self.confirm_var,
                show="●",
                width=30,
                style="App.TEntry"
            )
            self.confirm_entry.pack(fill=tk.X)
        
        # Button frame
        button_frame = ttk.Frame(form_frame, style="App.TFrame")
        button_frame.pack(pady=20)
        
        login_button = ttk.Button(
            button_frame,
            text="Login" if self.salt_exists else "Create Vault",
            command=self._handle_login,
            style="Accent.TButton",
            width=20
        )
        login_button.pack()
        
        # Info text
        info_text = (
            "Enter your master password to unlock your vault." if self.salt_exists 
            else "Create a strong master password to secure your vault. You won't be able to recover it if forgotten."
        )
        
        info_label = ttk.Label(
            container,
            text=info_text,
            font=("Helvetica", 10),
            foreground="#94A3B8",
            background="#1E293B",
            wraplength=400,
            justify=tk.CENTER
        )
        info_label.pack(pady=10)
        
        # Set focus to password entry
        self.password_entry.focus()
        
        # Bind enter key to login
        self.password_entry.bind("<Return>", lambda e: self._handle_login())
        if not self.salt_exists:
            self.confirm_entry.bind("<Return>", lambda e: self._handle_login())
    
    def _handle_login(self):
        """Handle the login or vault creation process"""
        password = self.password_var.get()
        
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            return
        
        if not self.salt_exists:
            # First-time setup - create new vault
            confirm_password = self.confirm_var.get()
            
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
                
            if len(password) < 8:
                messagebox.showerror("Error", "Master password must be at least 8 characters long")
                return
            
            try:
                # Create encryption handler with new master password
                encryption_handler = PasswordEncryption(password)
                password_store = PasswordStore(encryption_handler)
                messagebox.showinfo("Success", "Vault created successfully")
                self.on_login_callback(encryption_handler, password_store)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to create vault: {str(e)}")
        else:
            # Existing vault - validate password
            try:
                encryption_handler = PasswordEncryption(password)
                password_store = PasswordStore(encryption_handler)
                
                # Try to load and decrypt an entry to validate the password
                entries = password_store.get_all_entries(decrypt_passwords=True)
                
                # If we have entries but couldn't decrypt any of them, the password is wrong
                if entries and all(entry.get("password") == None for entry in entries):
                    messagebox.showerror("Error", "Incorrect master password")
                    return
                
                self.on_login_callback(encryption_handler, password_store)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to unlock vault: {str(e)}")