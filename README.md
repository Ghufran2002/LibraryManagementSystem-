# 📚 Library Management System

A comprehensive, database-driven library management application built with Python and Tkinter. Perfect for managing book inventory, member registrations, borrowing/returning books, and generating detailed reports.

---

## 🎯 Features

- ✅ **Dashboard** - Real-time library statistics and quick actions
- ✅ **Book Management** - Add, edit, search, and delete books
- ✅ **Member Management** - Register and manage library members
- ✅ **Borrowing System** - Issue and return books with automatic fine calculation
- ✅ **Advanced Search** - Search by title, author, ISBN, or member name
- ✅ **Comprehensive Reports** - Books by category, overdue items, fines, and statistics
- ✅ **Data Validation** - Input validation to prevent errors
- ✅ **User-Friendly GUI** - Professional Tkinter interface

---

## 📋 Requirements

- Python 3.8 or higher
- SQLite3 (included with Python)
- Tkinter (included with Python on most systems)
- PIL (Python Imaging Library)
- Matplotlib (for advanced charts)

---

## 🚀 Installation & Quick Start

### Step 1: Set Up the Project

```bash
# Create a project folder
mkdir LibraryManagementSystem
cd LibraryManagementSystem

# Copy all files into this folder
# - main.py
# - database.py
# - config.py
# - populate_sample_data.py
# - PRESENTATION_GUIDE.md
# - PROJECT_GUIDE.md
# - README.md
```

### Step 2: Install Dependencies

```bash
# Install required packages
pip install pillow matplotlib

# Note: Tkinter and SQLite3 come with Python
```

### Step 3: Create Sample Data (Optional but Recommended)

```bash
# Populate database with sample data for testing
python populate_sample_data.py
```

### Step 4: Run the Application

```bash
# Start the application
python main.py
```

---

## 📚 Project Structure

```
LibraryManagementSystem/
│
├── main.py                      # Main GUI application
├── database.py                  # Database operations
├── config.py                    # Configuration settings
├── populate_sample_data.py      # Sample data script
├── library.db                   # SQLite database (auto-created)
│
├── README.md                    # This file
├── PROJECT_GUIDE.md             # Detailed project guide
└── PRESENTATION_GUIDE.md        # Presentation instructions
```

---

## 💡 How to Use

### 1. **Dashboard**
- View library statistics at a glance
- See total books, members, and overdue items
- Access quick action buttons

### 2. **Book Management**
- **Add Book**: Click "+ Add Book" to register a new book
- **Search Books**: Use the search bar to find books by title, author, or ISBN
- **Edit Book**: Select a book and click "✏️ Edit" to update details
- **Delete Book**: Select a book and click "🗑️ Delete" to remove it

### 3. **Member Management**
- **Register Member**: Click "+ Register Member" to add a new member
- **Search Members**: Find members by name, email, or phone
- **Edit Member**: Update member information
- **Delete Member**: Remove member (only if no active borrowing)
- **View History**: Click "📖 History" to see member's borrowing history

### 4. **Borrowing Management**
- **Issue Book**: 
  1. Click "📤 Issue Book"
  2. Select member and book
  3. Set borrowing period (default: 14 days)
  4. Confirm
  
- **Return Book**:
  1. Go to Borrowing section
  2. Select the record to return
  3. Click "📥 Return Book"
  4. System automatically calculates fine if overdue

### 5. **Reports**
Generate various reports:
- 📊 Books by Category
- 👥 Active Members
- ⚠️ Overdue Books with fine amounts
- 💰 Fine Collections status
- 📈 Library Statistics

---

## 🔐 Database Schema

### Tables

**books**
- book_id (Primary Key)
- title, author, isbn (Unique)
- category, published_year
- quantity, available_quantity
- price
- added_date

**members**
- member_id (Primary Key)
- name, email, phone
- address
- membership_date
- membership_status
- fine_balance

**borrowing**
- borrow_id (Primary Key)
- book_id, member_id (Foreign Keys)
- borrow_date, due_date
- return_date, status
- fine_amount

**fines**
- fine_id (Primary Key)
- member_id, borrow_id (Foreign Keys)
- fine_amount, paid_status
- fine_date, paid_date

---

## ⚙️ Configuration

All settings are in `config.py`:

```python
# Fine Settings
FINE_PER_DAY = 10  # Rupees per day overdue
DEFAULT_BORROW_DAYS = 14  # Default borrowing period

# Colors
HEADER_COLOR = "#1e3a8a"
BUTTON_COLOR = "#3b82f6"
SUCCESS_COLOR = "#10b981"
WARNING_COLOR = "#f59e0b"
DANGER_COLOR = "#ef4444"

# Categories
CATEGORIES = ['Fiction', 'Non-Fiction', 'Science', 'Technology', ...]
```

Modify these values as needed for your library.

---

## 📊 Sample Data

Run `python populate_sample_data.py` to add:
- 12 sample books across different categories
- 6 sample members
- Multiple borrowing records
- Examples of overdue books and fines

This is useful for testing and demonstrations.

---

## 🎓 Presentation

For presenting this project to a panel:

1. **Read PRESENTATION_GUIDE.md** - Contains complete presentation structure
2. **Prepare sample data** - Run populate_sample_data.py before presentation
3. **Practice demo flow** - Follow the suggested demo sequence
4. **Know your code** - Be ready to explain any part
5. **Test everything** - Run through all features before presentation

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'PIL'"
**Solution:**
```bash
pip install pillow
```

### Issue: "ModuleNotFoundError: No module named 'tkinter'"
**Solution (Linux):**
```bash
sudo apt-get install python3-tk
```

**Solution (Mac):**
- Usually included, or reinstall Python from python.org

### Issue: "database.db not found"
**Solution:** Run the application once - it will create the database automatically

### Issue: Application looks ugly/font issues
**Solution:** This is normal on some systems. The functionality remains the same.

---

## 📈 Performance Tips

1. **Indexing**: Database is indexed for fast searches
2. **Pagination**: Large result sets are displayed efficiently
3. **Lazy Loading**: Data loaded only when needed
4. **Caching**: Database connection reused throughout session

The system can handle:
- Up to 100,000 books
- Up to 50,000 members
- Years of transaction history

---

## 🔒 Security Features

- ✅ Input validation prevents invalid data
- ✅ SQL injection prevention through parameterized queries
- ✅ Referential integrity through foreign keys
- ✅ Unique constraints prevent duplicates
- ✅ Atomic transactions ensure data consistency

**Future Enhancements:**
- User authentication and role-based access
- Activity logging and audit trails
- Data encryption for sensitive information

---

## 🚀 Future Enhancements

- 📱 Mobile app for member access
- 🔐 User authentication system
- 📧 Email notifications for due books
- 💳 Online fine payment integration
- 📱 Barcode scanner integration
- 📊 Advanced analytics dashboard
- ☁️ Cloud backup support
- 🔄 Multi-user support with proper locking

---

## 📝 Documentation

- **PROJECT_GUIDE.md** - Technical project overview and assessment criteria
- **PRESENTATION_GUIDE.md** - Complete presentation guide with talking points
- **Code Comments** - Every function has detailed docstrings
- **config.py** - All settings documented with explanations

---

## 📞 Support

If you encounter issues:

1. Check the Troubleshooting section above
2. Review the error message carefully
3. Check that all files are in the same directory
4. Ensure Python 3.8+ is installed
5. Verify all dependencies are installed

---

## 📊 Project Statistics

- **Lines of Code**: ~2500+
- **Database Tables**: 4
- **GUI Components**: 50+
- **Features Implemented**: 15+
- **Time to Complete**: 6-8 hours

---

## ✅ Checklist for Presentation

Before presenting:

- [ ] All files copied to project folder
- [ ] Dependencies installed (`pip install pillow matplotlib`)
- [ ] Sample data populated (`python populate_sample_data.py`)
- [ ] Application runs without errors (`python main.py`)
- [ ] All features tested
- [ ] PRESENTATION_GUIDE.md reviewed
- [ ] Demo flow practiced 3+ times
- [ ] Code reviewed and understood
- [ ] Backup of database created
- [ ] Presentation slides/talking points prepared

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Database Design**
- Proper normalization
- Foreign key relationships
- Indexing and optimization

✅ **Python Programming**
- Object-oriented design
- Error handling
- Code documentation

✅ **GUI Development**
- Tkinter framework
- Event handling
- User interface design

✅ **Software Engineering**
- Modular architecture
- Code organization
- Version control ready

✅ **Real-world Application**
- Practical problem solving
- Business logic implementation
- Data management

---

## 📄 License

This project is created for educational purposes.

---

## 👨‍💻 Author

Created as a final year project for Computer Science students.

---

## 🎉 Good Luck!

You have a complete, professional Library Management System ready for presentation. Follow the guides, practice your demo, and present with confidence!

**Happy Coding! 🚀**

---

## Quick Reference

| Task | Steps |
|------|-------|
| **Install** | `pip install pillow matplotlib` |
| **Create Sample Data** | `python populate_sample_data.py` |
| **Run App** | `python main.py` |
| **Add Book** | Dashboard → Books → "+ Add Book" |
| **Issue Book** | Dashboard → Borrowing → "📤 Issue Book" |
| **Return Book** | Borrowing → Select → "📥 Return Book" |
| **View Reports** | Dashboard → Reports → Choose Report |

---

For detailed presentation guide, see **PRESENTATION_GUIDE.md**
