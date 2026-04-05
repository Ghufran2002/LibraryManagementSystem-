"""
Database Operations Module for Library Management System
Handles all SQLite database operations with proper error handling
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any

class DatabaseManager:
    """Manages all database operations for the library system"""
    
    def __init__(self, db_name: str = 'library.db'):
        """Initialize database connection"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.init_database()
    
    def connect(self) -> None:
        """Create connection to database"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            raise Exception(f"Database connection error: {e}")
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
    
    def init_database(self) -> None:
        """Initialize database with tables if they don't exist"""
        self.connect()
        
        # Create Books table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                category TEXT NOT NULL,
                published_year INTEGER,
                quantity INTEGER NOT NULL,
                available_quantity INTEGER NOT NULL,
                price REAL,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create Members table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                membership_status TEXT DEFAULT 'Active',
                fine_balance REAL DEFAULT 0.0
            )
        ''')
        
        # Create Borrowing table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS borrowing (
                borrow_id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                member_id INTEGER NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP NOT NULL,
                return_date TIMESTAMP,
                fine_amount REAL DEFAULT 0.0,
                status TEXT DEFAULT 'Borrowed',
                FOREIGN KEY(book_id) REFERENCES books(book_id),
                FOREIGN KEY(member_id) REFERENCES members(member_id)
            )
        ''')
        
        # Create Fine table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS fines (
                fine_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                borrow_id INTEGER,
                fine_amount REAL NOT NULL,
                paid_status TEXT DEFAULT 'Unpaid',
                fine_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid_date TIMESTAMP,
                FOREIGN KEY(member_id) REFERENCES members(member_id),
                FOREIGN KEY(borrow_id) REFERENCES borrowing(borrow_id)
            )
        ''')
        
        self.connection.commit()
    
    # ============ BOOK OPERATIONS ============
    
    def add_book(self, title: str, author: str, isbn: str, category: str, 
                 published_year: int, quantity: int, price: float) -> bool:
        """Add new book to library"""
        try:
            self.cursor.execute('''
                INSERT INTO books (title, author, isbn, category, published_year, quantity, available_quantity, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, category, published_year, quantity, quantity, price))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding book: {e}")
            return False
    
    def get_all_books(self) -> List[Dict]:
        """Retrieve all books"""
        try:
            self.cursor.execute('SELECT * FROM books ORDER BY title')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
    
    def search_books(self, search_term: str) -> List[Dict]:
        """Search books by title, author, or ISBN"""
        try:
            query = '''SELECT * FROM books 
                      WHERE title LIKE ? OR author LIKE ? OR isbn LIKE ? 
                      ORDER BY title'''
            search_pattern = f'%{search_term}%'
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error searching books: {e}")
            return []
    
    def get_book_by_id(self, book_id: int) -> Dict:
        """Get book details by ID"""
        try:
            self.cursor.execute('SELECT * FROM books WHERE book_id = ?', (book_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching book: {e}")
            return None
    
    def update_book(self, book_id: int, title: str, author: str, isbn: str,
                   category: str, published_year: int, quantity: int, price: float) -> bool:
        """Update book information"""
        try:
            self.cursor.execute('''
                UPDATE books 
                SET title=?, author=?, isbn=?, category=?, published_year=?, quantity=?, price=?
                WHERE book_id=?
            ''', (title, author, isbn, category, published_year, quantity, price, book_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating book: {e}")
            return False
    
    def delete_book(self, book_id: int) -> bool:
        """Delete book from library"""
        try:
            self.cursor.execute('DELETE FROM books WHERE book_id = ?', (book_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting book: {e}")
            return False
    
    # ============ MEMBER OPERATIONS ============
    
    def add_member(self, name: str, email: str, phone: str, address: str) -> bool:
        """Register new member"""
        try:
            self.cursor.execute('''
                INSERT INTO members (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            ''', (name, email, phone, address))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding member: {e}")
            return False
    
    def get_all_members(self) -> List[Dict]:
        """Retrieve all members"""
        try:
            self.cursor.execute('SELECT * FROM members ORDER BY name')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching members: {e}")
            return []
    
    def search_members(self, search_term: str) -> List[Dict]:
        """Search members by name, email, or phone"""
        try:
            query = '''SELECT * FROM members 
                      WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? 
                      ORDER BY name'''
            search_pattern = f'%{search_term}%'
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error searching members: {e}")
            return []
    
    def get_member_by_id(self, member_id: int) -> Dict:
        """Get member details by ID"""
        try:
            self.cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except Exception as e:
            print(f"Error fetching member: {e}")
            return None
    
    def update_member(self, member_id: int, name: str, email: str, phone: str, address: str) -> bool:
        """Update member information"""
        try:
            self.cursor.execute('''
                UPDATE members 
                SET name=?, email=?, phone=?, address=?
                WHERE member_id=?
            ''', (name, email, phone, address, member_id))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating member: {e}")
            return False
    
    def delete_member(self, member_id: int) -> bool:
        """Delete member"""
        try:
            self.cursor.execute('DELETE FROM members WHERE member_id = ?', (member_id,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error deleting member: {e}")
            return False
    
    # ============ BORROWING OPERATIONS ============
    
    def issue_book(self, book_id: int, member_id: int, days_to_borrow: int = 14) -> bool:
        """Issue a book to member"""
        try:
            # Check if book is available
            book = self.get_book_by_id(book_id)
            if not book or book['available_quantity'] <= 0:
                return False
            
            # Calculate due date
            borrow_date = datetime.now()
            due_date = borrow_date + timedelta(days=days_to_borrow)
            
            # Insert borrowing record
            self.cursor.execute('''
                INSERT INTO borrowing (book_id, member_id, due_date)
                VALUES (?, ?, ?)
            ''', (book_id, member_id, due_date))
            
            # Update available quantity
            self.cursor.execute('''
                UPDATE books 
                SET available_quantity = available_quantity - 1
                WHERE book_id = ?
            ''', (book_id,))
            
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error issuing book: {e}")
            return False
    
    def return_book(self, borrow_id: int) -> Tuple[bool, float]:
        """Return a book and calculate fine if overdue"""
        try:
            # Get borrowing record
            self.cursor.execute('SELECT * FROM borrowing WHERE borrow_id = ?', (borrow_id,))
            record = self.cursor.fetchone()
            
            if not record:
                return False, 0
            
            # Calculate fine if overdue
            due_date = datetime.strptime(record['due_date'], '%Y-%m-%d %H:%M:%S')
            return_date = datetime.now()
            fine_amount = 0
            
            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                fine_amount = days_overdue * 10  # 10 per day
            
            # Update borrowing record
            self.cursor.execute('''
                UPDATE borrowing 
                SET return_date = ?, fine_amount = ?, status = 'Returned'
                WHERE borrow_id = ?
            ''', (return_date, fine_amount, borrow_id))
            
            # Update available quantity
            book_id = record['book_id']
            self.cursor.execute('''
                UPDATE books 
                SET available_quantity = available_quantity + 1
                WHERE book_id = ?
            ''', (book_id,))
            
            # Add fine record if applicable
            if fine_amount > 0:
                member_id = record['member_id']
                self.cursor.execute('''
                    INSERT INTO fines (member_id, borrow_id, fine_amount)
                    VALUES (?, ?, ?)
                ''', (member_id, borrow_id, fine_amount))
                
                # Update member's fine balance
                self.cursor.execute('''
                    UPDATE members 
                    SET fine_balance = fine_balance + ?
                    WHERE member_id = ?
                ''', (fine_amount, member_id))
            
            self.connection.commit()
            return True, fine_amount
        except Exception as e:
            print(f"Error returning book: {e}")
            return False, 0
    
    def get_active_borrowing(self) -> List[Dict]:
        """Get all active borrowing records"""
        try:
            self.cursor.execute('''
                SELECT b.*, bo.title, m.name as member_name 
                FROM borrowing b 
                JOIN books bo ON b.book_id = bo.book_id 
                JOIN members m ON b.member_id = m.member_id 
                WHERE b.status = 'Borrowed'
                ORDER BY b.due_date
            ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching borrowing records: {e}")
            return []
    
    def get_overdue_books(self) -> List[Dict]:
        """Get all overdue books"""
        try:
            self.cursor.execute('''
                SELECT b.*, bo.title, m.name as member_name,
                       CAST((julianday('now') - julianday(b.due_date)) AS INTEGER) as days_overdue
                FROM borrowing b 
                JOIN books bo ON b.book_id = bo.book_id 
                JOIN members m ON b.member_id = m.member_id 
                WHERE b.status = 'Borrowed' AND b.due_date < datetime('now')
                ORDER BY b.due_date
            ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching overdue books: {e}")
            return []
    
    # ============ STATISTICS & REPORTS ============
    
    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        try:
            stats = {}
            
            # Total books
            self.cursor.execute('SELECT COUNT(*) as count FROM books')
            stats['total_books'] = self.cursor.fetchone()['count']
            
            # Total members
            self.cursor.execute('SELECT COUNT(*) as count FROM members')
            stats['total_members'] = self.cursor.fetchone()['count']
            
            # Books borrowed
            self.cursor.execute('SELECT COUNT(*) as count FROM borrowing WHERE status = "Borrowed"')
            stats['books_borrowed'] = self.cursor.fetchone()['count']
            
            # Overdue books
            self.cursor.execute('''
                SELECT COUNT(*) as count FROM borrowing 
                WHERE status = 'Borrowed' AND due_date < datetime('now')
            ''')
            stats['overdue_books'] = self.cursor.fetchone()['count']
            
            return stats
        except Exception as e:
            print(f"Error getting dashboard stats: {e}")
            return {}
    
    def get_category_stats(self) -> List[Dict]:
        """Get books count by category"""
        try:
            self.cursor.execute('''
                SELECT category, COUNT(*) as count 
                FROM books 
                GROUP BY category
            ''')
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error getting category stats: {e}")
            return []
    
    def get_member_history(self, member_id: int) -> List[Dict]:
        """Get borrowing history for a member"""
        try:
            self.cursor.execute('''
                SELECT b.*, bo.title, bo.author
                FROM borrowing b 
                JOIN books bo ON b.book_id = bo.book_id 
                WHERE b.member_id = ?
                ORDER BY b.borrow_date DESC
            ''', (member_id,))
            return [dict(row) for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Error fetching member history: {e}")
            return []
