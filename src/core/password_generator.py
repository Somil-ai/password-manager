import random
import string
import re

class PasswordGenerator:
    """Class for generating secure random passwords"""
    
    def __init__(self):
        """Initialize the password generator"""
        self.lowercase_chars = string.ascii_lowercase
        self.uppercase_chars = string.ascii_uppercase
        self.digit_chars = string.digits
        self.special_chars = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    
    def generate_password(self, length=16, include_lowercase=True, 
                         include_uppercase=True, include_digits=True,
                         include_special=True):
        """Generate a random password based on specified criteria"""
        if length < 4 and (include_lowercase + include_uppercase + 
                           include_digits + include_special) > length:
            raise ValueError("Password length too short for required character types")
            
        if not any([include_lowercase, include_uppercase, include_digits, include_special]):
            raise ValueError("At least one character type must be selected")
        
        # Prepare the character pool based on options
        char_pool = ""
        if include_lowercase:
            char_pool += self.lowercase_chars
        if include_uppercase:
            char_pool += self.uppercase_chars
        if include_digits:
            char_pool += self.digit_chars
        if include_special:
            char_pool += self.special_chars
            
        # Ensure at least one character from each selected type
        password = []
        if include_lowercase:
            password.append(random.choice(self.lowercase_chars))
        if include_uppercase:
            password.append(random.choice(self.uppercase_chars))
        if include_digits:
            password.append(random.choice(self.digit_chars))
        if include_special:
            password.append(random.choice(self.special_chars))
            
        # Fill the rest of the password length
        remaining_length = length - len(password)
        password.extend(random.choice(char_pool) for _ in range(remaining_length))
        
        # Shuffle the password
        random.shuffle(password)
        
        return ''.join(password)
    
    def evaluate_strength(self, password):
        """Evaluate the strength of a password and return a score from 0-100"""
        if not password:
            return 0
            
        strength = 0
        # Length contribution (up to 40 points)
        length_score = min(len(password) * 2.5, 40)
        strength += length_score
        
        # Character variety (up to 60 points)
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_digits = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()-_=+\[\]{}|;:,.<>?/~]', password))
        
        char_type_count = has_lowercase + has_uppercase + has_digits + has_special
        variety_score = char_type_count * 15
        strength += variety_score
        
        # Return the total strength score (0-100)
        return min(round(strength), 100)
    
    def get_strength_category(self, score):
        """Get a category based on password strength score"""
        if score < 40:
            return "Weak"
        elif score < 70:
            return "Moderate"
        elif score < 90:
            return "Strong"
        else:
            return "Very Strong"