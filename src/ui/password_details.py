import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.password_generator_frame import PasswordGeneratorFrame

class PasswordDetailsFrame(ttk.Frame):
    """Frame for viewing and editing password details"""
    
    def __init__(self, parent, password_store, entry=None, is_new=False, callback=None):
        """Initialize the password details frame"""
        super().__init__(parent, style="App.TFrame")
        self.parent = parent
        self.password_store = password_store
        self.entry = entry
        self.is_new = is_new
        self.callback = callback
        
        # Set up variables
        self.title_var = tk.StringVar(value=entry["title"] if entry else "")
        self.username_var = tk.StringVar(value=entry["username"] if entry else "")
        self.password_var = tk.StringVar(value=entry["password"] if entry else "")
        self.website_var = tk.StringVar(value=entry["website"] if entry else "")
        self.category_var = tk.StringVar(value=entry["category"] if entry else "")
        self.notes_var = tk.StringVar(value=entry["notes"] if entry else "")
        self.show_password = tk.BooleanVar(value=False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the detail view widgets"""
        # Header
        header_label = ttk.Label(
            self,
            text="Password Details" if not self.is_new else "Add New Password",
            font=("Helvetica", 16, "bold"),
            style="App.TLabel"
        )
        header_label.pack(pady=(0, 20))
        
        # Form in a scrollable frame
        form_container = ttk.Frame(self, style="App.TFrame")
        form_container.pack(fill=tk.BOTH, expand=True)
        
        # Title field
        title_frame = ttk.Frame(form_container, style="App.TFrame")
        title_frame.pack(fill=tk.X, pady=5)
        
        title_label = ttk.Label(
            title_frame,
            text="Title:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        title_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_entry = ttk.Entry(
            title_frame,
            textvariable=self.title_var,
            width=40,
            style="App.TEntry"
        )
        title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Username field
        username_frame = ttk.Frame(form_container, style="App.TFrame")
        username_frame.pack(fill=tk.X, pady=5)
        
        username_label = ttk.Label(
            username_frame,
            text="Username:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        username_label.pack(side=tk.LEFT, padx=(0, 10))
        
        username_entry = ttk.Entry(
            username_frame,
            textvariable=self.username_var,
            width=40,
            style="App.TEntry"
        )
        username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password field
        password_frame = ttk.Frame(form_container, style="App.TFrame")
        password_frame.pack(fill=tk.X, pady=5)
        
        password_label = ttk.Label(
            password_frame,
            text="Password:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        password_label.pack(side=tk.LEFT, padx=(0, 10))
        
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            width=40,
            show="●",
            style="App.TEntry"
        )
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Password controls (show/hide, generate)
        pw_controls_frame = ttk.Frame(form_container, style="App.TFrame")
        pw_controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Empty label for alignment
        spacer = ttk.Label(
            pw_controls_frame,
            text="",
            width=15,
            style="App.TLabel"
        )
        spacer.pack(side=tk.LEFT)
        
        show_pw_check = ttk.Checkbutton(
            pw_controls_frame,
            text="Show Password",
            variable=self.show_password,
            command=self._toggle_password_visibility,
            style="App.TCheckbutton"
        )
        show_pw_check.pack(side=tk.LEFT, padx=(0, 10))
        
        generate_btn = ttk.Button(
            pw_controls_frame,
            text="Generate Password",
            command=self._generate_password,
            style="Accent.TButton"
        )
        generate_btn.pack(side=tk.LEFT)
        
        # Website field
        website_frame = ttk.Frame(form_container, style="App.TFrame")
        website_frame.pack(fill=tk.X, pady=5)
        
        website_label = ttk.Label(
            website_frame,
            text="Website:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        website_label.pack(side=tk.LEFT, padx=(0, 10))
        
        website_entry = ttk.Entry(
            website_frame,
            textvariable=self.website_var,
            width=40,
            style="App.TEntry"
        )
        website_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Category field
        category_frame = ttk.Frame(form_container, style="App.TFrame")
        category_frame.pack(fill=tk.X, pady=5)
        
        category_label = ttk.Label(
            category_frame,
            text="Category:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        category_label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Category combobox with existing categories + option to enter new
        categories = self.password_store.get_categories()
        category_combobox = ttk.Combobox(
            category_frame,
            textvariable=self.category_var,
            values=categories,
            width=38,
            style="App.TCombobox"
        )
        category_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Notes field
        notes_frame = ttk.Frame(form_container, style="App.TFrame")
        notes_frame.pack(fill=tk.X, pady=5)
        
        notes_label = ttk.Label(
            notes_frame,
            text="Notes:",
            width=15,
            anchor=tk.W,
            style="App.TLabel"
        )
        notes_label.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10), pady=5)
        
        notes_text = tk.Text(
            notes_frame,
            wrap=tk.WORD,
            width=40,
            height=5,
            background="#1E293B",
            foreground="#E2E8F0",
            insertbackground="#E2E8F0",
            relief=tk.FLAT,
            padx=8,
            pady=8
        )
        notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Fill notes text widget if there's content
        if self.entry and self.entry.get("notes"):
            notes_text.insert("1.0", self.entry["notes"])
        
        # Add scrollbar to notes
        notes_scrollbar = ttk.Scrollbar(
            notes_frame, 
            orient=tk.VERTICAL, 
            command=notes_text.yview
        )
        notes_text.configure(yscrollcommand=notes_scrollbar.set)
        notes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        button_frame = ttk.Frame(self, style="App.TFrame")
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            command=self._cancel,
            style="App.TButton",
            width=15
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        save_text = "Save Changes" if not self.is_new else "Add Password"
        save_btn = ttk.Button(
            button_frame,
            text=save_text,
            command=lambda: self._save_changes(notes_text.get("1.0", tk.END).strip()),
            style="Accent.TButton",
            width=15
        )
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    def _toggle_password_visibility(self):
        """Toggle password visibility between plain text and hidden"""
        for child in self.winfo_children():
            if isinstance(child, ttk.Frame):
                for widget in child.winfo_children():
                    if isinstance(widget, ttk.Entry) and widget.cget("textvariable") == str(self.password_var):
                        widget.configure(show="" if self.show_password.get() else "●")
    
    def _generate_password(self):
        """Open password generator dialog"""
        top = tk.Toplevel(self)
        top.title("Generate Password")
        top.minsize(400, 300)
        top.transient(self.parent)
        top.grab_set()
        
        generator_frame = PasswordGeneratorFrame(
            top, 
            callback=self._set_generated_password
        )
        generator_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _set_generated_password(self, password):
        """Set the generated password in the password field"""
        self.password_var.set(password)
    
    def _save_changes(self, notes):
        """Save the password entry changes"""
        title = self.title_var.get().strip()
        username = self.username_var.get().strip()
        password = self.password_var.get()
        website = self.website_var.get().strip()
        category = self.category_var.get().strip()
        
        # Validate required fields
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
            
        if not password:
            messagebox.showerror("Error", "Password is required")
            return
        
        try:
            if self.is_new:
                # Add new entry
                self.password_store.add_entry(
                    title=title,
                    username=username,
                    password=password,
                    website=website,
                    category=category,
                    notes=notes
                )
                messagebox.showinfo("Success", "Password added successfully")
            else:
                # Update existing entry
                self.password_store.update_entry(
                    entry_id=self.entry["id"],
                    title=title,
                    username=username,
                    password=password,
                    website=website,
                    category=category,
                    notes=notes
                )
                messagebox.showinfo("Success", "Password updated successfully")
            
            # Close the window and refresh parent
            if self.callback:
                self.callback()
            self.parent.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")
    
    def _cancel(self):
        """Cancel and close the dialog"""
        self.parent.destroy()