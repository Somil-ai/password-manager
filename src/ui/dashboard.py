import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import threading
import time
from src.ui.password_generator_frame import PasswordGeneratorFrame
from src.ui.password_details import PasswordDetailsFrame
from src.ui.utils import create_tooltip

class DashboardFrame(ttk.Frame):
    """Main dashboard frame for the password manager"""
    
    def __init__(self, parent, encryption_handler, password_store, logout_callback):
        """Initialize the dashboard frame"""
        super().__init__(parent, style="App.TFrame")
        self.parent = parent
        self.encryption_handler = encryption_handler
        self.password_store = password_store
        self.logout_callback = logout_callback
        
        # State variables
        self.selected_entry_id = None
        self.filter_text = tk.StringVar()
        self.filter_text.trace_add("write", self._filter_entries)
        self.selected_category = tk.StringVar()
        self.selected_category.trace_add("write", self._filter_entries)
        
        self._create_widgets()
        self._load_entries()
        self._load_categories()
    
    def _create_widgets(self):
        """Create the dashboard widgets"""
        # Create main panes
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left sidebar frame (categories & actions)
        self.sidebar_frame = ttk.Frame(self.paned_window, style="Sidebar.TFrame")
        
        # Main content area
        self.content_frame = ttk.Frame(self.paned_window, style="App.TFrame")
        
        self.paned_window.add(self.sidebar_frame, weight=1)
        self.paned_window.add(self.content_frame, weight=3)
        
        # Create the sidebar widgets
        self._create_sidebar()
        
        # Create the content area widgets
        self._create_content_area()
    
    def _create_sidebar(self):
        """Create the sidebar with actions and filters"""
        # App title and logout
        header_frame = ttk.Frame(self.sidebar_frame, style="Sidebar.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        app_title = ttk.Label(
            header_frame, 
            text="SecureVault", 
            font=("Helvetica", 16, "bold"),
            foreground="#3B82F6",
            background="#0F172A"
        )
        app_title.pack(side=tk.LEFT, padx=10, pady=10)
        
        logout_btn = ttk.Button(
            header_frame, 
            text="Logout", 
            command=self.logout_callback,
            style="Sidebar.TButton",
            width=8
        )
        logout_btn.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # Actions section
        actions_frame = ttk.LabelFrame(
            self.sidebar_frame,
            text="Actions",
            style="Sidebar.TLabelframe"
        )
        actions_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Add new password button
        add_btn = ttk.Button(
            actions_frame,
            text="Add New Password",
            command=self._add_new_password,
            style="Accent.TButton"
        )
        add_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Generate password button
        generate_btn = ttk.Button(
            actions_frame,
            text="Generate Password",
            command=self._show_password_generator,
            style="Sidebar.TButton"
        )
        generate_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Categories section
        categories_frame = ttk.LabelFrame(
            self.sidebar_frame,
            text="Categories",
            style="Sidebar.TLabelframe"
        )
        categories_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # All categories option
        all_categories_btn = ttk.Radiobutton(
            categories_frame,
            text="All Items",
            value="",
            variable=self.selected_category,
            style="Sidebar.TRadiobutton"
        )
        all_categories_btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Scrollable frame for categories
        categories_container = ttk.Frame(categories_frame, style="Sidebar.TFrame")
        categories_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create a canvas with scrollbar for categories
        self.categories_canvas = tk.Canvas(
            categories_container,
            background="#0F172A",
            highlightthickness=0
        )
        scrollbar = ttk.Scrollbar(
            categories_container,
            orient=tk.VERTICAL,
            command=self.categories_canvas.yview
        )
        
        self.categories_canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.categories_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Frame inside canvas for category buttons
        self.categories_list_frame = ttk.Frame(self.categories_canvas, style="Sidebar.TFrame")
        self.categories_canvas.create_window(
            (0, 0),
            window=self.categories_list_frame,
            anchor=tk.NW,
            width=self.categories_canvas.winfo_reqwidth()
        )
        
        self.categories_list_frame.bind("<Configure>", self._on_categories_configure)
        
        # Statistics section (optional)
        stats_frame = ttk.LabelFrame(
            self.sidebar_frame,
            text="Statistics",
            style="Sidebar.TLabelframe"
        )
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.total_passwords_var = tk.StringVar(value="Total Passwords: 0")
        total_label = ttk.Label(
            stats_frame,
            textvariable=self.total_passwords_var,
            style="Sidebar.TLabel"
        )
        total_label.pack(anchor=tk.W, padx=5, pady=2)
        
        self.categories_count_var = tk.StringVar(value="Categories: 0")
        categories_label = ttk.Label(
            stats_frame,
            textvariable=self.categories_count_var,
            style="Sidebar.TLabel"
        )
        categories_label.pack(anchor=tk.W, padx=5, pady=2)
    
    def _create_content_area(self):
        """Create the main content area"""
        # Search and filter bar
        search_frame = ttk.Frame(self.content_frame, style="App.TFrame")
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        search_label = ttk.Label(
            search_frame,
            text="Search:",
            style="App.TLabel"
        )
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.filter_text,
            width=30,
            style="App.TEntry"
        )
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Passwords list view
        list_frame = ttk.LabelFrame(
            self.content_frame,
            text="Stored Passwords",
            style="App.TLabelframe"
        )
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create treeview with scrollbar
        tree_frame = ttk.Frame(list_frame, style="App.TFrame")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Define columns
        columns = ("title", "username", "category", "website", "modified")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="App.Treeview"
        )
        
        # Define headings
        self.tree.heading("title", text="Title")
        self.tree.heading("username", text="Username")
        self.tree.heading("category", text="Category")
        self.tree.heading("website", text="Website")
        self.tree.heading("modified", text="Last Modified")
        
        # Column widths
        self.tree.column("title", width=150)
        self.tree.column("username", width=150)
        self.tree.column("category", width=100)
        self.tree.column("website", width=150)
        self.tree.column("modified", width=150)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Pack the tree and scrollbars
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Bind double-click event to view details
        self.tree.bind("<Double-1>", self._view_password_details)
        self.tree.bind("<<TreeviewSelect>>", self._on_treeview_select)
        
        # Details section at bottom
        self.details_frame = ttk.Frame(self.content_frame, style="App.TFrame")
        self.details_frame.pack(fill=tk.X, pady=10)
        
        # Detail actions frame
        details_buttons_frame = ttk.Frame(self.details_frame, style="App.TFrame")
        details_buttons_frame.pack(fill=tk.X)
        
        self.view_btn = ttk.Button(
            details_buttons_frame,
            text="View Details",
            command=lambda: self._view_password_details(None),
            state=tk.DISABLED,
            style="App.TButton"
        )
        self.view_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.edit_btn = ttk.Button(
            details_buttons_frame,
            text="Edit",
            command=self._edit_password,
            state=tk.DISABLED,
            style="App.TButton"
        )
        self.edit_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.copy_btn = ttk.Button(
            details_buttons_frame,
            text="Copy Password",
            command=self._copy_password,
            state=tk.DISABLED,
            style="App.TButton"
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.delete_btn = ttk.Button(
            details_buttons_frame,
            text="Delete",
            command=self._delete_password,
            state=tk.DISABLED,
            style="Warning.TButton"
        )
        self.delete_btn.pack(side=tk.RIGHT, padx=5, pady=5)
    
    def _load_entries(self):
        """Load password entries into the treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all entries
        entries = self.password_store.get_all_entries()
        
        # Update statistics
        self.total_passwords_var.set(f"Total Passwords: {len(entries)}")
        
        # Filter by category and search text if needed
        if self.selected_category.get():
            entries = [e for e in entries if e["category"] == self.selected_category.get()]
            
        filter_text = self.filter_text.get().lower()
        if filter_text:
            entries = [e for e in entries if (
                filter_text in e["title"].lower() or
                filter_text in e["username"].lower() or
                filter_text in e["website"].lower() or
                filter_text in e["category"].lower()
            )]
        
        # Add entries to treeview
        for entry in entries:
            # Format the date
            date_str = entry["modified_at"].split("T")[0]
            
            self.tree.insert(
                "",
                tk.END,
                iid=entry["id"],
                values=(
                    entry["title"],
                    entry["username"],
                    entry["category"],
                    entry["website"],
                    date_str
                )
            )
    
    def _load_categories(self):
        """Load categories into the sidebar"""
        # Clear existing category buttons
        for widget in self.categories_list_frame.winfo_children():
            widget.destroy()
        
        # Get categories and update statistics
        categories = self.password_store.get_categories()
        self.categories_count_var.set(f"Categories: {len(categories)}")
        
        # Add category buttons
        for category in categories:
            category_btn = ttk.Radiobutton(
                self.categories_list_frame,
                text=category,
                value=category,
                variable=self.selected_category,
                style="Sidebar.TRadiobutton"
            )
            category_btn.pack(fill=tk.X, padx=0, pady=2)
    
    def _on_categories_configure(self, event):
        """Update scrollregion when the categories frame changes size"""
        self.categories_canvas.configure(scrollregion=self.categories_canvas.bbox("all"))
    
    def _filter_entries(self, *args):
        """Filter entries based on search text and category"""
        self._load_entries()
    
    def _add_new_password(self):
        """Add a new password entry"""
        self._view_password_details(None, is_new=True)
    
    def _show_password_generator(self):
        """Show the password generator in a new window"""
        top = tk.Toplevel(self)
        top.title("Generate Password")
        top.minsize(400, 300)
        top.transient(self.master)
        top.grab_set()
        
        generator_frame = PasswordGeneratorFrame(top)
        generator_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _view_password_details(self, event, is_new=False):
        """View password details in a new window"""
        if not is_new and not self.selected_entry_id:
            return
            
        top = tk.Toplevel(self)
        top.title("Password Details" if not is_new else "Add New Password")
        top.minsize(500, 400)
        top.transient(self.master)
        top.grab_set()
        
        entry = None
        if not is_new:
            entry = self.password_store.get_entry(self.selected_entry_id)
        
        details_frame = PasswordDetailsFrame(
            top,
            self.password_store,
            entry,
            is_new,
            self._refresh_after_change
        )
        details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def _edit_password(self):
        """Edit the selected password entry"""
        if not self.selected_entry_id:
            return
        self._view_password_details(None)
    
    def _copy_password(self):
        """Copy the password to clipboard and clear after timeout"""
        if not self.selected_entry_id:
            return
            
        entry = self.password_store.get_entry(self.selected_entry_id)
        if entry and "password" in entry:
            pyperclip.copy(entry["password"])
            messagebox.showinfo("Password Copied", 
                               "Password copied to clipboard. It will be cleared in 30 seconds.")
            
            # Clear clipboard after 30 seconds
            threading.Timer(30, lambda: pyperclip.copy("")).start()
    
    def _delete_password(self):
        """Delete the selected password entry"""
        if not self.selected_entry_id:
            return
            
        entry = self.password_store.get_entry(self.selected_entry_id)
        if entry:
            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{entry['title']}'?\nThis action cannot be undone."
            )
            
            if confirm:
                if self.password_store.delete_entry(self.selected_entry_id):
                    self._refresh_after_change()
                    messagebox.showinfo("Success", "Password deleted successfully")
                else:
                    messagebox.showerror("Error", "Failed to delete password")
    
    def _on_treeview_select(self, event):
        """Handle treeview selection event"""
        selected_items = self.tree.selection()
        if selected_items:
            self.selected_entry_id = selected_items[0]
            self._update_buttons_state(True)
        else:
            self.selected_entry_id = None
            self._update_buttons_state(False)
    
    def _update_buttons_state(self, enable):
        """Update the state of action buttons based on selection"""
        state = tk.NORMAL if enable else tk.DISABLED
        self.view_btn.configure(state=state)
        self.edit_btn.configure(state=state)
        self.copy_btn.configure(state=state)
        self.delete_btn.configure(state=state)
    
    def _refresh_after_change(self):
        """Refresh the UI after a password entry is changed"""
        self._load_entries()
        self._load_categories()
        self.selected_entry_id = None
        self._update_buttons_state(False)