"""
Library Management System - Main GUI Application
Tkinter-based graphical interface for library operations
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
import database
import config
import re

class LibraryManagementApp:
    """Main application class for Library Management System"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title(config.APP_NAME)
        self.root.geometry(config.WINDOW_GEOMETRY)
        self.root.configure(bg=config.BG_COLOR)
        
        # Initialize database
        self.db = database.DatabaseManager(config.DATABASE_NAME)
        
        # Current view tracking
        self.current_frame = None
        
        # Setup UI
        self.setup_ui()
        self.show_dashboard()
    
    def clear_frame(self):
        """Clear current frame"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
    
    def setup_ui(self):
        """Setup main UI with menu bar"""
        # Top menu frame
        menu_frame = tk.Frame(self.root, bg=config.HEADER_COLOR, height=60)
        menu_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Title
        title_label = tk.Label(
            menu_frame, 
            text="📚 " + config.APP_NAME,
            font=("Segoe UI", 16, "bold"),
            bg=config.HEADER_COLOR,
            fg="white"
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        # Menu buttons
        buttons_frame = tk.Frame(menu_frame, bg=config.HEADER_COLOR)
        buttons_frame.pack(side=tk.RIGHT, padx=20, pady=10)
        
        menu_items = [
            ("Dashboard", self.show_dashboard),
            ("Books", self.show_books),
            ("Members", self.show_members),
            ("Borrowing", self.show_borrowing),
            ("Reports", self.show_reports),
        ]
        
        for label, command in menu_items:
            btn = tk.Button(
                buttons_frame,
                text=label,
                command=command,
                bg=config.BUTTON_COLOR,
                fg="white",
                font=config.BUTTON_FONT,
                relief=tk.FLAT,
                padx=15,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=5)
            
            # Hover effect
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=config.BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=config.BUTTON_COLOR))
        
        # Content frame
        self.content_frame = tk.Frame(self.root, bg=config.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # ============ DASHBOARD ============
    
    def show_dashboard(self):
        """Show dashboard with statistics"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.content_frame, bg=config.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(
            self.current_frame,
            text="Dashboard",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        title.pack(pady=10)
        
        # Get statistics
        stats = self.db.get_dashboard_stats()
        category_stats = self.db.get_category_stats()
        overdue = self.db.get_overdue_books()
        
        # Stats cards
        stats_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        stats_frame.pack(fill=tk.X, pady=20)
        
        stat_items = [
            ("Total Books", stats.get('total_books', 0), config.BUTTON_COLOR),
            ("Total Members", stats.get('total_members', 0), config.SUCCESS_COLOR),
            ("Books Borrowed", stats.get('books_borrowed', 0), config.WARNING_COLOR),
            ("Overdue Books", stats.get('overdue_books', 0), config.DANGER_COLOR),
        ]
        
        for label, value, color in stat_items:
            self.create_stat_card(stats_frame, label, value, color)
        
        # Category breakdown
        cat_frame = tk.Frame(self.current_frame, bg="white", relief=tk.RAISED, bd=1)
        cat_frame.pack(fill=tk.X, pady=10, padx=5)
        
        cat_label = tk.Label(
            cat_frame,
            text="📊 Books by Category",
            font=config.HEADER_FONT,
            bg="white",
            fg=config.TEXT_COLOR
        )
        cat_label.pack(anchor=tk.W, padx=10, pady=5)
        
        for cat in category_stats[:5]:
            cat_name = cat['category']
            cat_count = cat['count']
            cat_item = tk.Label(
                cat_frame,
                text=f"  {cat_name}: {cat_count} books",
                font=config.TEXT_FONT,
                bg="white",
                fg=config.TEXT_COLOR
            )
            cat_item.pack(anchor=tk.W, padx=20)
        
        # Quick links
        quick_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        quick_frame.pack(fill=tk.X, pady=20)
        
        quick_label = tk.Label(
            quick_frame,
            text="Quick Actions:",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        quick_label.pack(anchor=tk.W, padx=5)
        
        quick_buttons = [
            ("➕ Add Book", self.show_add_book),
            ("➕ Register Member", self.show_add_member),
            ("📤 Issue Book", self.show_issue_book),
            ("📥 Return Book", self.show_return_book),
        ]
        
        quick_btn_frame = tk.Frame(quick_frame, bg=config.BG_COLOR)
        quick_btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        for label, command in quick_buttons:
            btn = tk.Button(
                quick_btn_frame,
                text=label,
                command=command,
                bg=config.BUTTON_COLOR,
                fg="white",
                font=config.BUTTON_FONT,
                relief=tk.FLAT,
                padx=20,
                pady=10
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def create_stat_card(self, parent, label, value, color):
        """Create a statistics card"""
        card = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        card.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        value_label = tk.Label(
            card,
            text=str(value),
            font=("Segoe UI", 32, "bold"),
            bg=color,
            fg="white"
        )
        value_label.pack(pady=10)
        
        label_widget = tk.Label(
            card,
            text=label,
            font=config.LABEL_FONT,
            bg=color,
            fg="white"
        )
        label_widget.pack(pady=5)
    
    # ============ BOOKS MANAGEMENT ============
    
    def show_books(self):
        """Show books management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.content_frame, bg=config.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Book Management",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        title.pack(side=tk.LEFT)
        
        add_btn = tk.Button(
            header_frame,
            text="+ Add Book",
            command=self.show_add_book,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Search
        search_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Search:", bg=config.BG_COLOR, font=config.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=config.TEXT_FONT, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_books():
            term = search_var.get()
            self.populate_books_table(term if term else None)
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            command=search_books,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=10
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ("ID", "Title", "Author", "ISBN", "Category", "Available", "Price")
        self.books_table = ttk.Treeview(table_frame, columns=columns, height=config.TABLE_HEIGHT)
        self.books_table.column("#0", width=0, stretch=tk.NO)
        self.books_table.column("ID", anchor=tk.CENTER, width=40)
        self.books_table.column("Title", anchor=tk.W, width=200)
        self.books_table.column("Author", anchor=tk.W, width=150)
        self.books_table.column("ISBN", anchor=tk.CENTER, width=120)
        self.books_table.column("Category", anchor=tk.CENTER, width=100)
        self.books_table.column("Available", anchor=tk.CENTER, width=80)
        self.books_table.column("Price", anchor=tk.CENTER, width=80)
        
        self.books_table.heading("#0", text="", anchor=tk.W)
        self.books_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.books_table.heading("Title", text="Title", anchor=tk.W)
        self.books_table.heading("Author", text="Author", anchor=tk.W)
        self.books_table.heading("ISBN", text="ISBN", anchor=tk.CENTER)
        self.books_table.heading("Category", text="Category", anchor=tk.CENTER)
        self.books_table.heading("Available", text="Available", anchor=tk.CENTER)
        self.books_table.heading("Price", text="Price", anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.books_table.yview)
        self.books_table.configure(yscroll=scrollbar.set)
        
        self.books_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = tk.Button(
            action_frame,
            text="✏️ Edit",
            command=self.edit_book,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Delete",
            command=self.delete_book,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        # Load data
        self.populate_books_table()
    
    def populate_books_table(self, search_term=None):
        """Populate books table"""
        # Clear table
        for item in self.books_table.get_children():
            self.books_table.delete(item)
        
        # Get books
        if search_term:
            books = self.db.search_books(search_term)
        else:
            books = self.db.get_all_books()
        
        # Add to table
        for book in books:
            self.books_table.insert(
                parent='',
                index='end',
                values=(
                    book['book_id'],
                    book['title'],
                    book['author'],
                    book['isbn'],
                    book['category'],
                    book['available_quantity'],
                    f"₹{book['price']:.2f}"
                )
            )
    
    def show_add_book(self):
        """Show add book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Book")
        dialog.geometry("500x500")
        dialog.configure(bg=config.BG_COLOR)
        
        # Form fields
        fields = {
            'title': 'Title',
            'author': 'Author',
            'isbn': 'ISBN',
            'category': 'Category',
            'year': 'Published Year',
            'quantity': 'Quantity',
            'price': 'Price'
        }
        
        entries = {}
        
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(dialog, text=label + ":", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=10
            )
            
            if key == 'category':
                var = tk.StringVar()
                combo = ttk.Combobox(dialog, textvariable=var, values=config.CATEGORIES, font=config.TEXT_FONT, width=30)
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = var
            else:
                entry = tk.Entry(dialog, font=config.TEXT_FONT, width=30)
                entry.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = entry
        
        def save():
            try:
                # Validation
                if not all([entries[k].get() if not isinstance(entries[k], tk.StringVar) else entries[k].get() for k in fields]):
                    messagebox.showerror("Error", config.MSG_ERROR_EMPTY)
                    return
                
                title = entries['title'].get()
                author = entries['author'].get()
                isbn = entries['isbn'].get()
                category = entries['category'].get()
                year = int(entries['year'].get())
                quantity = int(entries['quantity'].get())
                price = float(entries['price'].get())
                
                if len(title) < config.MIN_NAME_LENGTH or len(author) < config.MIN_NAME_LENGTH:
                    messagebox.showerror("Error", "Title and Author must be at least 3 characters")
                    return
                
                if self.db.add_book(title, author, isbn, category, year, quantity, price):
                    messagebox.showinfo("Success", config.MSG_SUCCESS_ADD)
                    dialog.destroy()
                    self.show_books()
                else:
                    messagebox.showerror("Error", "Failed to add book. ISBN might be duplicate.")
            except ValueError:
                messagebox.showerror("Error", config.MSG_ERROR_INVALID_INPUT)
        
        # Buttons
        btn_frame = tk.Frame(dialog, bg=config.BG_COLOR)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="Save",
            command=save,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
    
    def edit_book(self):
        """Edit selected book"""
        selection = self.books_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to edit")
            return
        
        item = self.books_table.item(selection[0])
        book_id = item['values'][0]
        
        book = self.db.get_book_by_id(book_id)
        if not book:
            messagebox.showerror("Error", config.MSG_ERROR_NOT_FOUND)
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Book")
        dialog.geometry("500x500")
        dialog.configure(bg=config.BG_COLOR)
        
        fields = {
            'title': 'Title',
            'author': 'Author',
            'isbn': 'ISBN',
            'category': 'Category',
            'year': 'Published Year',
            'quantity': 'Quantity',
            'price': 'Price'
        }
        
        entries = {}
        
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(dialog, text=label + ":", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=10
            )
            
            if key == 'category':
                var = tk.StringVar(value=book[key])
                combo = ttk.Combobox(dialog, textvariable=var, values=config.CATEGORIES, font=config.TEXT_FONT, width=30)
                combo.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = var
            else:
                entry = tk.Entry(dialog, font=config.TEXT_FONT, width=30)
                entry.insert(0, str(book[key]))
                entry.grid(row=i, column=1, padx=10, pady=10)
                entries[key] = entry
        
        def update():
            try:
                title = entries['title'].get()
                author = entries['author'].get()
                isbn = entries['isbn'].get()
                category = entries['category'].get()
                year = int(entries['year'].get())
                quantity = int(entries['quantity'].get())
                price = float(entries['price'].get())
                
                if self.db.update_book(book_id, title, author, isbn, category, year, quantity, price):
                    messagebox.showinfo("Success", config.MSG_SUCCESS_UPDATE)
                    dialog.destroy()
                    self.show_books()
                else:
                    messagebox.showerror("Error", "Failed to update book")
            except ValueError:
                messagebox.showerror("Error", config.MSG_ERROR_INVALID_INPUT)
        
        btn_frame = tk.Frame(dialog, bg=config.BG_COLOR)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="Update",
            command=update,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
    
    def delete_book(self):
        """Delete selected book"""
        selection = self.books_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        item = self.books_table.item(selection[0])
        book_id = item['values'][0]
        title = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Delete '{title}'?"):
            if self.db.delete_book(book_id):
                messagebox.showinfo("Success", config.MSG_SUCCESS_DELETE)
                self.show_books()
            else:
                messagebox.showerror("Error", "Failed to delete book")
    
    # ============ MEMBERS MANAGEMENT ============
    
    def show_members(self):
        """Show members management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.content_frame, bg=config.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Member Management",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        title.pack(side=tk.LEFT)
        
        add_btn = tk.Button(
            header_frame,
            text="+ Register Member",
            command=self.show_add_member,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        add_btn.pack(side=tk.RIGHT, padx=5)
        
        # Search
        search_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        search_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(search_frame, text="Search:", bg=config.BG_COLOR, font=config.LABEL_FONT).pack(side=tk.LEFT, padx=5)
        
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=config.TEXT_FONT, width=40)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        def search_members():
            term = search_var.get()
            self.populate_members_table(term if term else None)
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Search",
            command=search_members,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=10
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ("ID", "Name", "Email", "Phone", "Status", "Fine Balance")
        self.members_table = ttk.Treeview(table_frame, columns=columns, height=config.TABLE_HEIGHT)
        self.members_table.column("#0", width=0, stretch=tk.NO)
        self.members_table.column("ID", anchor=tk.CENTER, width=40)
        self.members_table.column("Name", anchor=tk.W, width=150)
        self.members_table.column("Email", anchor=tk.W, width=180)
        self.members_table.column("Phone", anchor=tk.CENTER, width=120)
        self.members_table.column("Status", anchor=tk.CENTER, width=100)
        self.members_table.column("Fine Balance", anchor=tk.CENTER, width=120)
        
        self.members_table.heading("#0", text="", anchor=tk.W)
        self.members_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.members_table.heading("Name", text="Name", anchor=tk.W)
        self.members_table.heading("Email", text="Email", anchor=tk.W)
        self.members_table.heading("Phone", text="Phone", anchor=tk.CENTER)
        self.members_table.heading("Status", text="Status", anchor=tk.CENTER)
        self.members_table.heading("Fine Balance", text="Fine Balance", anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.members_table.yview)
        self.members_table.configure(yscroll=scrollbar.set)
        
        self.members_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        action_frame.pack(fill=tk.X, pady=10)
        
        edit_btn = tk.Button(
            action_frame,
            text="✏️ Edit",
            command=self.edit_member,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        edit_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(
            action_frame,
            text="🗑️ Delete",
            command=self.delete_member,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        delete_btn.pack(side=tk.LEFT, padx=5)
        
        history_btn = tk.Button(
            action_frame,
            text="📖 History",
            command=self.show_member_history,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        history_btn.pack(side=tk.LEFT, padx=5)
        
        # Load data
        self.populate_members_table()
    
    def populate_members_table(self, search_term=None):
        """Populate members table"""
        # Clear table
        for item in self.members_table.get_children():
            self.members_table.delete(item)
        
        # Get members
        if search_term:
            members = self.db.search_members(search_term)
        else:
            members = self.db.get_all_members()
        
        # Add to table
        for member in members:
            self.members_table.insert(
                parent='',
                index='end',
                values=(
                    member['member_id'],
                    member['name'],
                    member['email'],
                    member['phone'],
                    member['membership_status'],
                    f"₹{member['fine_balance']:.2f}"
                )
            )
    
    def show_add_member(self):
        """Show add member dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Register Member")
        dialog.geometry("500x400")
        dialog.configure(bg=config.BG_COLOR)
        
        fields = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address'
        }
        
        entries = {}
        
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(dialog, text=label + ":", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=10
            )
            
            entry = tk.Entry(dialog, font=config.TEXT_FONT, width=30)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        def save():
            try:
                if not all([entries[k].get() for k in fields]):
                    messagebox.showerror("Error", config.MSG_ERROR_EMPTY)
                    return
                
                name = entries['name'].get()
                email = entries['email'].get()
                phone = entries['phone'].get()
                address = entries['address'].get()
                
                if len(name) < config.MIN_NAME_LENGTH:
                    messagebox.showerror("Error", "Name must be at least 3 characters")
                    return
                
                if len(phone) < config.MIN_PHONE_LENGTH:
                    messagebox.showerror("Error", f"Phone must be at least {config.MIN_PHONE_LENGTH} characters")
                    return
                
                if email and not re.match(config.EMAIL_PATTERN, email):
                    messagebox.showerror("Error", "Invalid email format")
                    return
                
                if self.db.add_member(name, email, phone, address):
                    messagebox.showinfo("Success", config.MSG_SUCCESS_ADD)
                    dialog.destroy()
                    self.show_members()
                else:
                    messagebox.showerror("Error", "Failed to add member")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = tk.Frame(dialog, bg=config.BG_COLOR)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="Register",
            command=save,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
    
    def edit_member(self):
        """Edit selected member"""
        selection = self.members_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a member to edit")
            return
        
        item = self.members_table.item(selection[0])
        member_id = item['values'][0]
        
        member = self.db.get_member_by_id(member_id)
        if not member:
            messagebox.showerror("Error", config.MSG_ERROR_NOT_FOUND)
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Member")
        dialog.geometry("500x400")
        dialog.configure(bg=config.BG_COLOR)
        
        fields = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone',
            'address': 'Address'
        }
        
        entries = {}
        
        for i, (key, label) in enumerate(fields.items()):
            tk.Label(dialog, text=label + ":", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
                row=i, column=0, sticky=tk.W, padx=10, pady=10
            )
            
            entry = tk.Entry(dialog, font=config.TEXT_FONT, width=30)
            entry.insert(0, member[key] if member[key] else "")
            entry.grid(row=i, column=1, padx=10, pady=10)
            entries[key] = entry
        
        def update():
            try:
                name = entries['name'].get()
                email = entries['email'].get()
                phone = entries['phone'].get()
                address = entries['address'].get()
                
                if self.db.update_member(member_id, name, email, phone, address):
                    messagebox.showinfo("Success", config.MSG_SUCCESS_UPDATE)
                    dialog.destroy()
                    self.show_members()
                else:
                    messagebox.showerror("Error", "Failed to update member")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = tk.Frame(dialog, bg=config.BG_COLOR)
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="Update",
            command=update,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
    
    def delete_member(self):
        """Delete selected member"""
        selection = self.members_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a member to delete")
            return
        
        item = self.members_table.item(selection[0])
        member_id = item['values'][0]
        name = item['values'][1]
        
        if messagebox.askyesno("Confirm", f"Delete member '{name}'?"):
            if self.db.delete_member(member_id):
                messagebox.showinfo("Success", config.MSG_SUCCESS_DELETE)
                self.show_members()
            else:
                messagebox.showerror("Error", "Failed to delete member")
    
    def show_member_history(self):
        """Show member borrowing history"""
        selection = self.members_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a member")
            return
        
        item = self.members_table.item(selection[0])
        member_id = item['values'][0]
        member_name = item['values'][1]
        
        history = self.db.get_member_history(member_id)
        
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Borrowing History - {member_name}")
        dialog.geometry("700x500")
        dialog.configure(bg=config.BG_COLOR)
        
        # Create treeview
        columns = ("ID", "Book Title", "Author", "Borrow Date", "Return Date", "Status")
        table = ttk.Treeview(dialog, columns=columns, height=20)
        table.column("#0", width=0, stretch=tk.NO)
        table.column("ID", anchor=tk.CENTER, width=40)
        table.column("Book Title", anchor=tk.W, width=200)
        table.column("Author", anchor=tk.W, width=150)
        table.column("Borrow Date", anchor=tk.CENTER, width=120)
        table.column("Return Date", anchor=tk.CENTER, width=120)
        table.column("Status", anchor=tk.CENTER, width=80)
        
        table.heading("#0", text="", anchor=tk.W)
        table.heading("ID", text="ID", anchor=tk.CENTER)
        table.heading("Book Title", text="Book Title", anchor=tk.W)
        table.heading("Author", text="Author", anchor=tk.W)
        table.heading("Borrow Date", text="Borrow Date", anchor=tk.CENTER)
        table.heading("Return Date", text="Return Date", anchor=tk.CENTER)
        table.heading("Status", text="Status", anchor=tk.CENTER)
        
        for record in history:
            table.insert(
                parent='',
                index='end',
                values=(
                    record['borrow_id'],
                    record['title'],
                    record['author'],
                    record['borrow_date'][:10],
                    record['return_date'][:10] if record['return_date'] else "N/A",
                    record['status']
                )
            )
        
        table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # ============ BORROWING OPERATIONS ============
    
    def show_borrowing(self):
        """Show borrowing management screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.content_frame, bg=config.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        header_frame.pack(fill=tk.X, pady=10)
        
        title = tk.Label(
            header_frame,
            text="Borrowing Management",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        title.pack(side=tk.LEFT)
        
        issue_btn = tk.Button(
            header_frame,
            text="📤 Issue Book",
            command=self.show_issue_book,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        issue_btn.pack(side=tk.RIGHT, padx=5)
        
        # Tabs for different views
        tab_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        tab_frame.pack(fill=tk.X, pady=10)
        
        def show_active():
            self.populate_borrowing_table("active")
        
        def show_overdue():
            self.populate_borrowing_table("overdue")
        
        tk.Button(
            tab_frame,
            text="📋 Active Borrowing",
            command=show_active,
            bg=config.BUTTON_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            tab_frame,
            text="⚠️ Overdue Books",
            command=show_overdue,
            bg=config.WARNING_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        # Table frame
        table_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create treeview
        columns = ("ID", "Member", "Book", "Borrow Date", "Due Date", "Days Left")
        self.borrowing_table = ttk.Treeview(table_frame, columns=columns, height=config.TABLE_HEIGHT)
        self.borrowing_table.column("#0", width=0, stretch=tk.NO)
        self.borrowing_table.column("ID", anchor=tk.CENTER, width=40)
        self.borrowing_table.column("Member", anchor=tk.W, width=150)
        self.borrowing_table.column("Book", anchor=tk.W, width=200)
        self.borrowing_table.column("Borrow Date", anchor=tk.CENTER, width=120)
        self.borrowing_table.column("Due Date", anchor=tk.CENTER, width=120)
        self.borrowing_table.column("Days Left", anchor=tk.CENTER, width=80)
        
        self.borrowing_table.heading("#0", text="", anchor=tk.W)
        self.borrowing_table.heading("ID", text="ID", anchor=tk.CENTER)
        self.borrowing_table.heading("Member", text="Member", anchor=tk.W)
        self.borrowing_table.heading("Book", text="Book", anchor=tk.W)
        self.borrowing_table.heading("Borrow Date", text="Borrow Date", anchor=tk.CENTER)
        self.borrowing_table.heading("Due Date", text="Due Date", anchor=tk.CENTER)
        self.borrowing_table.heading("Days Left", text="Days Left", anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.borrowing_table.yview)
        self.borrowing_table.configure(yscroll=scrollbar.set)
        
        self.borrowing_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Action buttons
        action_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        action_frame.pack(fill=tk.X, pady=10)
        
        return_btn = tk.Button(
            action_frame,
            text="📥 Return Book",
            command=self.show_return_book_selection,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=15
        )
        return_btn.pack(side=tk.LEFT, padx=5)
        
        # Load data
        self.populate_borrowing_table("active")
    
    def populate_borrowing_table(self, view_type="active"):
        """Populate borrowing table"""
        # Clear table
        for item in self.borrowing_table.get_children():
            self.borrowing_table.delete(item)
        
        # Get borrowing records
        if view_type == "active":
            records = self.db.get_active_borrowing()
        elif view_type == "overdue":
            records = self.db.get_overdue_books()
        else:
            records = []
        
        # Add to table
        for record in records:
            due_date = datetime.strptime(record['due_date'], '%Y-%m-%d %H:%M:%S')
            days_left = (due_date - datetime.now()).days
            
            self.borrowing_table.insert(
                parent='',
                index='end',
                values=(
                    record['borrow_id'],
                    record['member_name'],
                    record['title'],
                    record['borrow_date'][:10],
                    record['due_date'][:10],
                    days_left
                )
            )
    
    def show_issue_book(self):
        """Show issue book dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Issue Book")
        dialog.geometry("500x300")
        dialog.configure(bg=config.BG_COLOR)
        
        # Member selection
        tk.Label(dialog, text="Select Member:", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
            row=0, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        members = self.db.get_all_members()
        member_list = [f"{m['member_id']} - {m['name']}" for m in members]
        member_var = tk.StringVar()
        member_combo = ttk.Combobox(dialog, textvariable=member_var, values=member_list, font=config.TEXT_FONT, width=40)
        member_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Book selection
        tk.Label(dialog, text="Select Book:", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
            row=1, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        books = self.db.get_all_books()
        book_list = [f"{b['book_id']} - {b['title']}" for b in books if b['available_quantity'] > 0]
        book_var = tk.StringVar()
        book_combo = ttk.Combobox(dialog, textvariable=book_var, values=book_list, font=config.TEXT_FONT, width=40)
        book_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Days to borrow
        tk.Label(dialog, text="Days to Borrow:", font=config.LABEL_FONT, bg=config.BG_COLOR).grid(
            row=2, column=0, sticky=tk.W, padx=10, pady=10
        )
        
        days_entry = tk.Entry(dialog, font=config.TEXT_FONT, width=40)
        days_entry.insert(0, str(config.DEFAULT_BORROW_DAYS))
        days_entry.grid(row=2, column=1, padx=10, pady=10)
        
        def issue():
            try:
                if not member_var.get() or not book_var.get():
                    messagebox.showerror("Error", config.MSG_ERROR_EMPTY)
                    return
                
                member_id = int(member_var.get().split(' - ')[0])
                book_id = int(book_var.get().split(' - ')[0])
                days = int(days_entry.get())
                
                if self.db.issue_book(book_id, member_id, days):
                    messagebox.showinfo("Success", "Book issued successfully!")
                    dialog.destroy()
                    self.show_borrowing()
                else:
                    messagebox.showerror("Error", config.MSG_ERROR_BOOK_UNAVAILABLE)
            except ValueError:
                messagebox.showerror("Error", config.MSG_ERROR_INVALID_INPUT)
        
        btn_frame = tk.Frame(dialog, bg=config.BG_COLOR)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        tk.Button(
            btn_frame,
            text="Issue",
            command=issue,
            bg=config.SUCCESS_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg=config.DANGER_COLOR,
            fg="white",
            font=config.BUTTON_FONT,
            relief=tk.FLAT,
            padx=20
        ).pack(side=tk.LEFT, padx=5)
    
    def show_return_book_selection(self):
        """Show return book selection dialog"""
        selection = self.borrowing_table.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a record to return")
            return
        
        item = self.borrowing_table.item(selection[0])
        borrow_id = item['values'][0]
        
        success, fine = self.db.return_book(borrow_id)
        if success:
            msg = f"Book returned successfully!"
            if fine > 0:
                msg += f"\n\nFine Applied: ₹{fine:.2f}\n(₹{config.FINE_PER_DAY} per day overdue)"
            messagebox.showinfo("Success", msg)
            self.show_borrowing()
        else:
            messagebox.showerror("Error", "Failed to return book")
    
    def show_return_book(self):
        """Alternative return book method"""
        self.show_borrowing()
    
    # ============ REPORTS ============
    
    def show_reports(self):
        """Show reports screen"""
        self.clear_frame()
        
        self.current_frame = tk.Frame(self.content_frame, bg=config.BG_COLOR)
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        title = tk.Label(
            self.current_frame,
            text="Reports & Analytics",
            font=config.HEADER_FONT,
            bg=config.BG_COLOR,
            fg=config.TEXT_COLOR
        )
        title.pack(pady=20)
        
        # Report options
        reports_frame = tk.Frame(self.current_frame, bg=config.BG_COLOR)
        reports_frame.pack(fill=tk.BOTH, expand=True)
        
        report_items = [
            ("📊 Books by Category", self.report_books_by_category),
            ("👥 Active Members", self.report_active_members),
            ("⚠️ Overdue Books", self.report_overdue_books),
            ("💰 Fine Collections", self.report_fines),
            ("📈 Library Statistics", self.report_statistics),
        ]
        
        for label, command in report_items:
            btn = tk.Button(
                reports_frame,
                text=label,
                command=command,
                bg=config.BUTTON_COLOR,
                fg="white",
                font=config.BUTTON_FONT,
                relief=tk.FLAT,
                padx=30,
                pady=15,
                width=30
            )
            btn.pack(pady=10)
    
    def report_books_by_category(self):
        """Generate books by category report"""
        categories = self.db.get_category_stats()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Books by Category Report")
        dialog.geometry("500x400")
        dialog.configure(bg=config.BG_COLOR)
        
        text = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "=" * 50 + "\n")
        text.insert(tk.END, "BOOKS BY CATEGORY REPORT\n")
        text.insert(tk.END, "=" * 50 + "\n\n")
        
        total = sum([c['count'] for c in categories])
        
        for cat in categories:
            percentage = (cat['count'] / total * 100) if total > 0 else 0
            text.insert(tk.END, f"{cat['category']:<30} {cat['count']:>5} ({percentage:>5.1f}%)\n")
        
        text.insert(tk.END, "\n" + "-" * 50 + "\n")
        text.insert(tk.END, f"{'TOTAL':<30} {total:>5}\n")
        text.config(state=tk.DISABLED)
    
    def report_active_members(self):
        """Generate active members report"""
        members = self.db.get_all_members()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Active Members Report")
        dialog.geometry("700x500")
        dialog.configure(bg=config.BG_COLOR)
        
        text = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "=" * 90 + "\n")
        text.insert(tk.END, "ACTIVE MEMBERS REPORT\n")
        text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text.insert(tk.END, "=" * 90 + "\n\n")
        
        text.insert(tk.END, f"{'ID':<5} {'Name':<20} {'Email':<30} {'Phone':<15} {'Status':<10}\n")
        text.insert(tk.END, "-" * 90 + "\n")
        
        for member in members:
            text.insert(tk.END, f"{member['member_id']:<5} {member['name']:<20} {member['email']:<30} {member['phone']:<15} {member['membership_status']:<10}\n")
        
        text.insert(tk.END, "-" * 90 + "\n")
        text.insert(tk.END, f"Total Members: {len(members)}\n")
        text.config(state=tk.DISABLED)
    
    def report_overdue_books(self):
        """Generate overdue books report"""
        overdue = self.db.get_overdue_books()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Overdue Books Report")
        dialog.geometry("900x500")
        dialog.configure(bg=config.BG_COLOR)
        
        text = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "=" * 120 + "\n")
        text.insert(tk.END, "OVERDUE BOOKS REPORT\n")
        text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text.insert(tk.END, "=" * 120 + "\n\n")
        
        text.insert(tk.END, f"{'ID':<6} {'Member':<15} {'Book':<30} {'Due Date':<12} {'Days OD':<8} {'Fine':<10}\n")
        text.insert(tk.END, "-" * 120 + "\n")
        
        total_fine = 0
        for record in overdue:
            fine = record['days_overdue'] * config.FINE_PER_DAY
            total_fine += fine
            text.insert(tk.END, f"{record['borrow_id']:<6} {record['member_name']:<15} {record['title']:<30} {record['due_date'][:10]:<12} {record['days_overdue']:<8} ₹{fine:<9.2f}\n")
        
        text.insert(tk.END, "-" * 120 + "\n")
        text.insert(tk.END, f"Total Overdue: {len(overdue)} | Total Fine: ₹{total_fine:.2f}\n")
        text.config(state=tk.DISABLED)
    
    def report_fines(self):
        """Generate fine collections report"""
        members = self.db.get_all_members()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Fine Collections Report")
        dialog.geometry("600x400")
        dialog.configure(bg=config.BG_COLOR)
        
        text = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "=" * 70 + "\n")
        text.insert(tk.END, "FINE COLLECTIONS REPORT\n")
        text.insert(tk.END, "=" * 70 + "\n\n")
        
        text.insert(tk.END, f"{'ID':<5} {'Name':<25} {'Fine Balance':<15}\n")
        text.insert(tk.END, "-" * 70 + "\n")
        
        total_fine = 0
        for member in members:
            if member['fine_balance'] > 0:
                text.insert(tk.END, f"{member['member_id']:<5} {member['name']:<25} ₹{member['fine_balance']:<14.2f}\n")
                total_fine += member['fine_balance']
        
        text.insert(tk.END, "-" * 70 + "\n")
        text.insert(tk.END, f"Total Fine Outstanding: ₹{total_fine:.2f}\n")
        text.config(state=tk.DISABLED)
    
    def report_statistics(self):
        """Generate library statistics report"""
        stats = self.db.get_dashboard_stats()
        books = self.db.get_all_books()
        members = self.db.get_all_members()
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Library Statistics Report")
        dialog.geometry("600x500")
        dialog.configure(bg=config.BG_COLOR)
        
        text = tk.Text(dialog, font=("Courier", 10), bg="white", fg="black")
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, "=" * 60 + "\n")
        text.insert(tk.END, "LIBRARY STATISTICS REPORT\n")
        text.insert(tk.END, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        text.insert(tk.END, "=" * 60 + "\n\n")
        
        text.insert(tk.END, "COLLECTION STATISTICS:\n")
        text.insert(tk.END, "-" * 60 + "\n")
        text.insert(tk.END, f"Total Books in Library:       {stats.get('total_books', 0)}\n")
        
        total_available = sum([b['available_quantity'] for b in books])
        text.insert(tk.END, f"Total Available Books:        {total_available}\n")
        text.insert(tk.END, f"Total Borrowed Books:         {stats.get('books_borrowed', 0)}\n")
        
        text.insert(tk.END, "\nMEMBERSHIP STATISTICS:\n")
        text.insert(tk.END, "-" * 60 + "\n")
        text.insert(tk.END, f"Total Members:                {stats.get('total_members', 0)}\n")
        
        active_members = len([m for m in members if m['membership_status'] == 'Active'])
        text.insert(tk.END, f"Active Members:               {active_members}\n")
        
        text.insert(tk.END, "\nOVERDUE STATISTICS:\n")
        text.insert(tk.END, "-" * 60 + "\n")
        text.insert(tk.END, f"Overdue Books:                {stats.get('overdue_books', 0)}\n")
        
        text.config(state=tk.DISABLED)

def main():
    """Main entry point"""
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
