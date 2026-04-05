"""
Configuration Settings for Library Management System
"""

# Application Settings
APP_NAME = "Library Management System"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+100+100"

# Database Settings
DATABASE_NAME = 'library.db'

# Color Scheme
BG_COLOR = "#f0f0f0"
HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#3b82f6"
BUTTON_HOVER = "#2563eb"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
DANGER_COLOR = "#ef4444"
TEXT_COLOR = "#1f2937"
BORDER_COLOR = "#e5e7eb"

# Fine Settings
FINE_PER_DAY = 10  # Rupees per day
DEFAULT_BORROW_DAYS = 14

# Font Settings
HEADER_FONT = ("Segoe UI", 14, "bold")
LABEL_FONT = ("Segoe UI", 11)
TEXT_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 10, "bold")

# Table Settings
TABLE_HEIGHT = 15
TABLE_COLUMNS_WIDTH = {
    'book_id': 50,
    'member_id': 50,
    'borrow_id': 50,
    'title': 200,
    'author': 150,
    'name': 150,
    'email': 150,
    'phone': 100,
    'category': 100,
    'status': 80,
    'due_date': 120,
}

# Validation Rules
MIN_NAME_LENGTH = 3
MAX_NAME_LENGTH = 100
MIN_PHONE_LENGTH = 10
CATEGORIES = [
    'Fiction',
    'Non-Fiction',
    'Science',
    'Mathematics',
    'History',
    'Biography',
    'Technology',
    'Self-Help',
    'Education',
    'Other'
]

# Messages
MSG_SUCCESS_ADD = "Record added successfully!"
MSG_SUCCESS_UPDATE = "Record updated successfully!"
MSG_SUCCESS_DELETE = "Record deleted successfully!"
MSG_ERROR_EMPTY = "Please fill all required fields!"
MSG_ERROR_DUPLICATE = "This record already exists!"
MSG_ERROR_NOT_FOUND = "Record not found!"
MSG_ERROR_BOOK_UNAVAILABLE = "This book is not available!"
MSG_ERROR_INVALID_INPUT = "Invalid input! Please check your entries."

# Email Validation Pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
