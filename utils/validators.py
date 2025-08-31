"""
Form validation utilities
Helper functions for validating user input
"""

import re
import logging

logger = logging.getLogger(__name__)

def validate_email(email):
    """
    Validate email address format
    
    Args:
        email: Email address string
    
    Returns:
        bool: True if valid, False otherwise
    """
    if not email:
        return True  # Email is optional
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    return bool(re.match(pattern, email))

def validate_message(message):
    """
    Validate message content
    
    Args:
        message: Message string
    
    Returns:
        tuple: (is_valid, error_message)
    """
    if not message or not message.strip():
        return False, "Message cannot be empty"
    
    if len(message) > 5000:
        return False, "Message is too long (max 5000 characters)"
    
    # Check for potential spam patterns
    spam_patterns = [
        r'(?i)viagra',
        r'(?i)casino',
        r'(?i)winner.*prize',
        r'(?i)click.*here.*now'
    ]
    
    for pattern in spam_patterns:
        if re.search(pattern, message):
            logger.warning(f"Potential spam detected: {pattern}")
            # You might want to flag but not reject
            pass
    
    return True, None

def sanitize_input(text):
    """
    Sanitize user input to prevent XSS
    
    Args:
        text: Input text
    
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove or escape potentially dangerous characters
    replacements = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#x27;',
        '/': '&#x2F;'
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    return text.strip()

def validate_contact_form(form_data):
    """
    Validate entire contact form
    
    Args:
        form_data: Dictionary of form fields
    
    Returns:
        tuple: (is_valid, errors_dict)
    """
    errors = {}
    
    # Validate name (optional)
    name = form_data.get('name', '').strip()
    if name and len(name) > 100:
        errors['name'] = "Name is too long (max 100 characters)"
    
    # Validate email
    email = form_data.get('email', '').strip()
    if email and not validate_email(email):
        errors['email'] = "Invalid email address"
    
    # Validate message
    message = form_data.get('message', '').strip()
    is_valid, error_msg = validate_message(message)
    if not is_valid:
        errors['message'] = error_msg
    
    return len(errors) == 0, errors
