import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import threading
from src.core.password_generator import PasswordGenerator

class PasswordGeneratorFrame(ttk.Frame):
    """Frame for generating secure passwords"""
    
    def __init__(self, parent, callback=None):
        """Initialize the password generator frame"""
        super().__init__(parent, style="App.TFrame")
        self.parent = parent
        self.callback = callback
        self.generator = PasswordGenerator()
        
        # Set up variables
        self.password_var = tk.StringVar()
        self.length_var = tk.IntVar(value=16)
        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_special = tk.BooleanVar(value=True)
        self.strength_var = tk.IntVar(value=0)
        self.strength_text_var = tk.StringVar(value="")
        
        self._create_widgets()
        self._generate()  # Generate an initial password
    
    def _create_widgets(self):
        """Create the generator UI widgets"""
        # Title
        title_label = ttk.Label(
            self,
            text="Generate Secure Password",
            font=("Helvetica", 16, "bold"),
            style="App.TLabel"
        )
        title_label.pack(pady=(0, 15))
        
        # Generated password display
        password_frame = ttk.Frame(self, style="App.TFrame")
        password_frame.pack(fill=tk.X, padx=20, pady=10)
        
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=("Courier", 14),
            style="Password.TEntry",
            justify=tk.CENTER
        )
        password_entry.pack(fill=tk.X, pady=5)
        
        # Strength meter
        strength_frame = ttk.Frame(self, style="App.TFrame")
        strength_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        strength_label = ttk.Label(
            strength_frame,
            text="Strength:",
            style="App.TLabel"
        )
        strength_label.pack(side=tk.LEFT, padx=(0, 5))
        
        strength_value = ttk.Label(
            strength_frame,
            textvariable=self.strength_text_var,
            font=("Helvetica", 12, "bold"),
            style="App.TLabel"
        )
        strength_value.pack(side=tk.RIGHT)
        
        # Strength progress bar
        strength_progress = ttk.Progressbar(
            self,
            variable=self.strength_var,
            mode="determinate",
            length=300,
            maximum=100
        )
        strength_progress.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Options frame
        options_frame = ttk.LabelFrame(
            self,
            text="Password Options",
            style="App.TLabelframe"
        )
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Length slider
        length_frame = ttk.Frame(options_frame, style="App.TFrame")
        length_frame.pack(fill=tk.X, padx=10, pady=10)
        
        length_label = ttk.Label(
            length_frame,
            text="Length:",
            style="App.TLabel"
        )
        length_label.pack(side=tk.LEFT, padx=(0, 10))
        
        length_slider = ttk.Scale(
            length_frame,
            from_=8,
            to=32,
            variable=self.length_var,
            command=self._on_length_change,
            orient=tk.HORIZONTAL,
            length=200
        )
        length_slider.pack(side=tk.LEFT)
        
        length_value = ttk.Label(
            length_frame,
            textvariable=self.length_var,
            width=3,
            style="App.TLabel"
        )
        length_value.pack(side=tk.LEFT, padx=10)
        
        # Character options
        char_frame = ttk.Frame(options_frame, style="App.TFrame")
        char_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Character checkboxes in a grid
        lowercase_check = ttk.Checkbutton(
            char_frame,
            text="Lowercase (a-z)",
            variable=self.use_lowercase,
            command=self._on_option_change,
            style="App.TCheckbutton"
        )
        lowercase_check.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        uppercase_check = ttk.Checkbutton(
            char_frame,
            text="Uppercase (A-Z)",
            variable=self.use_uppercase,
            command=self._on_option_change,
            style="App.TCheckbutton"
        )
        uppercase_check.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        digits_check = ttk.Checkbutton(
            char_frame,
            text="Digits (0-9)",
            variable=self.use_digits,
            command=self._on_option_change,
            style="App.TCheckbutton"
        )
        digits_check.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        special_check = ttk.Checkbutton(
            char_frame,
            text="Special (!@#$%^&*)",
            variable=self.use_special,
            command=self._on_option_change,
            style="App.TCheckbutton"
        )
        special_check.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Buttons frame
        button_frame = ttk.Frame(self, style="App.TFrame")
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        generate_btn = ttk.Button(
            button_frame,
            text="Generate New",
            command=self._generate,
            style="Accent.TButton",
            width=15
        )
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = ttk.Button(
            button_frame,
            text="Copy to Clipboard",
            command=self._copy_to_clipboard,
            style="App.TButton",
            width=15
        )
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        if self.callback:
            use_btn = ttk.Button(
                button_frame,
                text="Use Password",
                command=self._use_password,
                style="App.TButton",
                width=15
            )
            use_btn.pack(side=tk.RIGHT, padx=5)
    
    def _on_length_change(self, event):
        """Handle length slider change event"""
        self._generate()
    
    def _on_option_change(self):
        """Handle character option checkbox changes"""
        # Ensure at least one option is selected
        if not any([
            self.use_lowercase.get(),
            self.use_uppercase.get(),
            self.use_digits.get(),
            self.use_special.get()
        ]):
            messagebox.showwarning(
                "Warning",
                "At least one character type must be selected"
            )
            self.use_lowercase.set(True)
        
        self._generate()
    
    def _generate(self):
        """Generate a new password with current settings"""
        try:
            password = self.generator.generate_password(
                length=self.length_var.get(),
                include_lowercase=self.use_lowercase.get(),
                include_uppercase=self.use_uppercase.get(),
                include_digits=self.use_digits.get(),
                include_special=self.use_special.get()
            )
            
            self.password_var.set(password)
            
            # Evaluate and display password strength
            strength = self.generator.evaluate_strength(password)
            self.strength_var.set(strength)
            
            category = self.generator.get_strength_category(strength)
            self.strength_text_var.set(category)
            
            # Set color based on strength
            strength_color = "#EF4444"  # Red for weak
            if strength >= 90:
                strength_color = "#10B981"  # Green for very strong
            elif strength >= 70:
                strength_color = "#3B82F6"  # Blue for strong
            elif strength >= 40:
                strength_color = "#F59E0B"  # Amber for moderate
                
            for child in self.winfo_children():
                if isinstance(child, ttk.Frame):
                    for widget in child.winfo_children():
                        if isinstance(widget, ttk.Label) and widget.cget("textvariable") == str(self.strength_text_var):
                            widget.configure(foreground=strength_color)
                            break
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _copy_to_clipboard(self):
        """Copy the generated password to clipboard"""
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo(
                "Copied to Clipboard",
                "Password has been copied to clipboard. It will be cleared in 30 seconds."
            )
            
            # Clear clipboard after 30 seconds
            threading.Timer(30, lambda: pyperclip.copy("")).start()
    
    def _use_password(self):
        """Use the generated password"""
        if self.callback:
            self.callback(self.password_var.get())
            self.parent.destroy()