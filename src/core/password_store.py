import json
import os
from datetime import datetime
import uuid
from src.core.encryption import PasswordEncryption

class PasswordStore:
    """Class for storing and retrieving password entries"""
    
    def __init__(self, encryption_handler):
        """Initialize the password store with an encryption handler"""
        self.encryption = encryption_handler
        self.data_dir = os.path.join(os.path.expanduser("~"), ".securevault")
        self.data_file = os.path.join(self.data_dir, "passwords.json")
        self.entries = self._load_entries()
        
    def _load_entries(self):
        """Load password entries from storage"""
        os.makedirs(self.data_dir, exist_ok=True)
        
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def _save_entries(self):
        """Save password entries to storage"""
        with open(self.data_file, "w") as f:
            json.dump(self.entries, f, indent=2)
    
    def add_entry(self, title, username, password, website="", category="", notes=""):
        """Add a new password entry"""
        entry_id = str(uuid.uuid4())
        encrypted_password = self.encryption.encrypt(password)
        
        new_entry = {
            "id": entry_id,
            "title": title,
            "username": username,
            "password": encrypted_password,
            "website": website,
            "category": category,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "modified_at": datetime.now().isoformat()
        }
        
        self.entries.append(new_entry)
        self._save_entries()
        return entry_id
    
    def get_entry(self, entry_id):
        """Get a password entry by ID"""
        for entry in self.entries:
            if entry["id"] == entry_id:
                # Create a copy of the entry to avoid modifying the original
                entry_copy = entry.copy()
                # Decrypt the password
                decrypted_password = self.encryption.decrypt(entry["password"])
                if decrypted_password:
                    entry_copy["password"] = decrypted_password
                return entry_copy
        return None
    
    def update_entry(self, entry_id, title=None, username=None, password=None, 
                    website=None, category=None, notes=None):
        """Update an existing password entry"""
        for i, entry in enumerate(self.entries):
            if entry["id"] == entry_id:
                if title is not None:
                    self.entries[i]["title"] = title
                if username is not None:
                    self.entries[i]["username"] = username
                if password is not None:
                    self.entries[i]["password"] = self.encryption.encrypt(password)
                if website is not None:
                    self.entries[i]["website"] = website
                if category is not None:
                    self.entries[i]["category"] = category
                if notes is not None:
                    self.entries[i]["notes"] = notes
                
                self.entries[i]["modified_at"] = datetime.now().isoformat()
                self._save_entries()
                return True
        return False
    
    def delete_entry(self, entry_id):
        """Delete a password entry by ID"""
        for i, entry in enumerate(self.entries):
            if entry["id"] == entry_id:
                del self.entries[i]
                self._save_entries()
                return True
        return False
    
    def get_all_entries(self, decrypt_passwords=False):
        """Get all password entries"""
        entries_copy = []
        for entry in self.entries:
            entry_copy = entry.copy()
            if decrypt_passwords:
                decrypted_password = self.encryption.decrypt(entry["password"])
                if decrypted_password:
                    entry_copy["password"] = decrypted_password
            entries_copy.append(entry_copy)
        return entries_copy
    
    def search_entries(self, query, categories=None):
        """Search for password entries by title, username, website, or notes"""
        results = []
        query = query.lower()
        
        for entry in self.entries:
            if categories and entry["category"] not in categories:
                continue
                
            if (query in entry["title"].lower() or
                query in entry["username"].lower() or
                query in entry["website"].lower() or
                query in entry["notes"].lower()):
                results.append(entry.copy())
        
        return results
    
    def get_categories(self):
        """Get a list of all categories in use"""
        categories = set()
        for entry in self.entries:
            if entry["category"]:
                categories.add(entry["category"])
        return sorted(list(categories))