"""
Sample Data Population Script
Run this to pre-populate the database with sample data for testing/demo
"""

import database
from datetime import datetime, timedelta
import random

def populate_sample_data():
    """Populate database with sample data"""
    db = database.DatabaseManager()
    
    print("Populating sample data...")
    
    # Sample Books
    books_data = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "978-0743273565", "Fiction", 1925, 5, 299.99),
        ("To Kill a Mockingbird", "Harper Lee", "978-0061120084", "Fiction", 1960, 4, 349.99),
        ("1984", "George Orwell", "978-0451524935", "Fiction", 1949, 3, 279.99),
        ("Python Crash Course", "Eric Matthes", "978-1593279288", "Technology", 2015, 6, 599.99),
        ("Introduction to Algorithms", "Cormen, Leiserson", "978-0262033848", "Technology", 2009, 2, 1299.99),
        ("The Selfish Gene", "Richard Dawkins", "978-0198788607", "Science", 1976, 3, 449.99),
        ("A Brief History of Time", "Stephen Hawking", "978-0553380163", "Science", 1988, 4, 399.99),
        ("Sapiens", "Yuval Noah Harari", "978-0062316097", "Non-Fiction", 2014, 5, 599.99),
        ("Educated", "Tara Westover", "978-0399590504", "Biography", 2018, 3, 499.99),
        ("Atomic Habits", "James Clear", "978-0735211292", "Self-Help", 2018, 4, 349.99),
        ("The Power of Now", "Eckhart Tolle", "978-0743245509", "Self-Help", 1997, 3, 279.99),
        ("Thinking, Fast and Slow", "Daniel Kahneman", "978-0374275631", "Psychology", 2011, 2, 549.99),
    ]
    
    print(f"Adding {len(books_data)} books...")
    for title, author, isbn, category, year, quantity, price in books_data:
        db.add_book(title, author, isbn, category, year, quantity, price)
    print("✓ Books added")
    
    # Sample Members
    members_data = [
        ("Raj Kumar", "raj.kumar@email.com", "9876543210", "New Delhi"),
        ("Priya Sharma", "priya.sharma@email.com", "9876543211", "New Delhi"),
        ("Amit Singh", "amit.singh@email.com", "9876543212", "Bangalore"),
        ("Neha Gupta", "neha.gupta@email.com", "9876543213", "Mumbai"),
        ("Vikram Patel", "vikram.patel@email.com", "9876543214", "Pune"),
        ("Anjali Verma", "anjali.verma@email.com", "9876543215", "Hyderabad"),
    ]
    
    print(f"Adding {len(members_data)} members...")
    for name, email, phone, address in members_data:
        db.add_member(name, email, phone, address)
    print("✓ Members added")
    
    # Sample Borrowing Records
    print("Adding borrowing records...")
    
    # Get books and members
    books = db.get_all_books()
    members = db.get_all_members()
    
    if books and members:
        # Active borrowing - Normal
        db.issue_book(books[0]['book_id'], members[0]['member_id'], 14)
        
        # Active borrowing - Due soon
        db.issue_book(books[1]['book_id'], members[1]['member_id'], 2)
        
        # Overdue borrowing (for demo purposes)
        db.issue_book(books[2]['book_id'], members[2]['member_id'], -5)  # Overdue by 5 days
        
        # Recently returned
        borrow_id = None
        db.cursor.execute('SELECT borrow_id FROM borrowing WHERE status = "Borrowed" LIMIT 1')
        result = db.cursor.fetchone()
        if result:
            borrow_id = result[0]
        
        if borrow_id:
            db.return_book(borrow_id)
        
        print("✓ Borrowing records added")
    
    db.disconnect()
    print("\n✅ Sample data population complete!")
    print("\nSample data added:")
    print(f"  - {len(books_data)} books")
    print(f"  - {len(members_data)} members")
    print(f"  - 4 borrowing records (1 overdue for demo)")
    print("\nYou can now run: python main.py")

if __name__ == "__main__":
    populate_sample_data()
