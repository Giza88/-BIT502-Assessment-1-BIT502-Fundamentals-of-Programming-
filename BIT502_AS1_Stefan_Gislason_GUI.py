

"""
Course code: BIT502
Assessment: Assessment 1
My full name: Stefan Gislason
My student number: LG-4785366286

GUI Version - Library Management System (Kiosk Style)
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional
from datetime import datetime

# Import constants and utility functions from the original file
from BIT502_AS1_Stefan_Gislason import (
    STANDARD_MONTHLY, PREMIUM_MONTHLY, KIDS_MONTHLY,
    ANNUAL_DISCOUNT_MONTHS,
    EXTRA_BOOK_RENTAL_COST, EXTRA_PRIVATE_AREA_COST,
    EXTRA_MONTHLY_BOOKLET_COST, EXTRA_ONLINE_EBOOK_RENTAL_COST,
    READING_CHALLENGE_WEEKLY_RECORD,
    RANK_THRESHOLD_BRONZE_MAX, RANK_THRESHOLD_SILVER_MAX, RANK_THRESHOLD_GOLD_MAX,
    RENTAL_RATE_DAYS_1_3, RENTAL_RATE_DAYS_4_8, RENTAL_RATE_DAYS_9_PLUS,
    RENTAL_MIN_DAYS, RENTAL_MAX_DAYS, RENTAL_FIXED_COST_21_DAYS,
    format_currency
)


class LibraryManagementGUI:
    """Main GUI application for Library Management System - Kiosk Style."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management Kiosk")
        # Set window size to fit nicely on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        # Use 90% of screen size for better fit
        window_width = int(screen_width * 0.9)
        window_height = int(screen_height * 0.9)
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg="#1a1a1a")
        
        # Cart to store selections
        self.cart = {
            'membership': None,  # {'type': 'STANDARD', 'name': 'Standard', 'cost': 15.00}
            'extras': [],  # List of {'name': str, 'cost': float}
            'rental': None,  # {'days': int, 'cost': float}
            'reading_challenge': None  # Just for tracking, no cost
        }
        
        # Style configuration
        self.setup_styles()
        
        # Create main container
        self.create_main_menu()
    
    def setup_styles(self):
        """Configure styles for kiosk/cash register look."""
        style = ttk.Style()
        style.theme_use('clam')
    
    def clear_frame(self):
        """Clear all widgets from the root window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def create_navigation_bar(self):
        """Create a navigation bar with Home, Cart, and Checkout buttons at the bottom of root window."""
        # Create nav bar directly on root window - fixed height and always visible
        nav_frame = tk.Frame(self.root, bg="#34495e", height=90)
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X)
        nav_frame.pack_propagate(False)
        
        nav_buttons_frame = tk.Frame(nav_frame, bg="#34495e")
        nav_buttons_frame.pack(pady=20)
        
        home_btn = tk.Button(
            nav_buttons_frame,
            text="HOME",
            command=self.create_main_menu,
            font=('Arial', 16, 'bold'),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        home_btn.pack(side=tk.LEFT, padx=20)
        
        cart_btn = tk.Button(
            nav_buttons_frame,
            text="VIEW CART",
            command=self.show_cart,
            font=('Arial', 16, 'bold'),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        cart_btn.pack(side=tk.LEFT, padx=20)
        
        checkout_btn = tk.Button(
            nav_buttons_frame,
            text="CHECKOUT",
            command=self.show_checkout,
            font=('Arial', 16, 'bold'),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        checkout_btn.pack(side=tk.LEFT, padx=20)
    
    def create_receipt_display(self, parent_frame):
        """Create a cash register receipt-style display area."""
        # Receipt frame (right side - like a cash register display)
        receipt_frame = tk.Frame(parent_frame, bg="#000000", relief=tk.RAISED, borderwidth=3)
        receipt_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False, padx=5, pady=5)
        receipt_frame.config(width=350)
        
        # Receipt header (like cash register) - fixed height to prevent cutoff
        receipt_header = tk.Frame(receipt_frame, bg="#000000", height=80)
        receipt_header.pack(fill=tk.X, padx=5, pady=(5, 0))
        receipt_header.pack_propagate(False)
        
        header_label = tk.Label(
            receipt_header,
            text="═══════════════════════",
            font=('Courier', 10),
            bg="#000000",
            fg="#00ff00"
        )
        header_label.pack(pady=(5, 2))
        
        title_label = tk.Label(
            receipt_header,
            text="LIBRARY KIOSK",
            font=('Courier', 12, 'bold'),
            bg="#000000",
            fg="#00ff00"
        )
        title_label.pack(pady=2)
        
        date_label = tk.Label(
            receipt_header,
            text=datetime.now().strftime("%Y-%m-%d %H:%M"),
            font=('Courier', 9),
            bg="#000000",
            fg="#00ff00"
        )
        date_label.pack(pady=2)
        
        separator = tk.Label(
            receipt_header,
            text="═══════════════════════",
            font=('Courier', 10),
            bg="#000000",
            fg="#00ff00"
        )
        separator.pack(pady=(2, 5))
        
        # Receipt display area (scrollable)
        receipt_display_frame = tk.Frame(receipt_frame, bg="#000000")
        receipt_display_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollable text area
        self.receipt_text = scrolledtext.ScrolledText(
            receipt_display_frame,
            font=('Courier', 10),
            bg="#000000",
            fg="#00ff00",
            width=40,
            height=30,
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0,
            insertbackground="#00ff00"
        )
        self.receipt_text.pack(fill=tk.BOTH, expand=True)
        self.receipt_text.config(state=tk.DISABLED)
        
        # Total display (like cash register total)
        total_frame = tk.Frame(receipt_frame, bg="#000000", relief=tk.RAISED, borderwidth=2)
        total_frame.pack(fill=tk.X, padx=5, pady=5)
        
        total_label = tk.Label(
            total_frame,
            text="TOTAL:",
            font=('Courier', 14, 'bold'),
            bg="#000000",
            fg="#ffff00"
        )
        total_label.pack(pady=5)
        
        self.total_display = tk.Label(
            total_frame,
            text="$0.00",
            font=('Courier', 18, 'bold'),
            bg="#000000",
            fg="#ffff00"
        )
        self.total_display.pack(pady=5)
        
        # Cart button
        cart_btn = tk.Button(
            receipt_frame,
            text="VIEW CART",
            command=self.show_cart,
            font=('Arial', 12, 'bold'),
            bg="#ff6600",
            fg="white",
            activebackground="#ff4400",
            width=30,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        cart_btn.pack(pady=10, padx=5)
        
        # Checkout button
        checkout_btn = tk.Button(
            receipt_frame,
            text="CHECKOUT",
            command=self.show_checkout,
            font=('Arial', 14, 'bold'),
            bg="#00aa00",
            fg="white",
            activebackground="#008800",
            width=30,
            height=3,
            relief=tk.RAISED,
            cursor="hand2"
        )
        checkout_btn.pack(pady=10, padx=5)
        
        self.update_receipt_display()
    
    def update_receipt_display(self):
        """Update the receipt display with current cart contents."""
        self.receipt_text.config(state=tk.NORMAL)
        self.receipt_text.delete(1.0, tk.END)
        
        receipt_lines = []
        receipt_lines.append("═══════════════════════\n")
        receipt_lines.append("LIBRARY KIOSK\n")
        receipt_lines.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        receipt_lines.append("═══════════════════════\n\n")
        
        total = 0.00
        
        # Membership
        if self.cart['membership']:
            membership = self.cart['membership']
            receipt_lines.append(f"Membership:\n")
            receipt_lines.append(f"  {membership['name']}\n")
            receipt_lines.append(f"  {format_currency(membership['cost'])}/mo\n")
            total += membership['cost']
            receipt_lines.append("\n")
        
        # Extras
        if self.cart['extras']:
            receipt_lines.append("Extras:\n")
            for extra in self.cart['extras']:
                receipt_lines.append(f"  {extra['name']}\n")
                receipt_lines.append(f"  {format_currency(extra['cost'])}/mo\n")
                total += extra['cost']
            receipt_lines.append("\n")
        
        # Rental
        if self.cart['rental']:
            rental = self.cart['rental']
            receipt_lines.append("Rental:\n")
            receipt_lines.append(f"  {rental['days']} days\n")
            receipt_lines.append(f"  {format_currency(rental['cost'])}\n")
            total += rental['cost']
            receipt_lines.append("\n")
        
        if total == 0.00:
            receipt_lines.append("Cart is empty\n")
            receipt_lines.append("Select items to add\n")
        
        receipt_lines.append("═══════════════════════\n")
        
        self.receipt_text.insert(1.0, "".join(receipt_lines))
        self.receipt_text.config(state=tk.DISABLED)
        
        # Update total display
        self.total_display.config(text=format_currency(total))
    
    def create_main_menu(self):
        """Create the main menu interface - Kiosk style."""
        self.clear_frame()
        
        # Create navigation bar FIRST
        self.create_navigation_bar()
        
        # Main container with split layout - leave space for nav bar
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 90))
        
        # Left side - Menu area
        menu_area = tk.Frame(main_container, bg="#2a2a2a")
        menu_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = tk.Frame(menu_area, bg="#ff6600", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="LIBRARY MANAGEMENT KIOSK",
            font=('Arial', 28, 'bold'),
            bg="#ff6600",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Menu content
        content_frame = tk.Frame(menu_area, bg="#2a2a2a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Menu label
        menu_label = tk.Label(
            content_frame,
            text="SELECT AN OPTION",
            font=('Arial', 16, 'bold'),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        menu_label.pack(pady=10)
        
        # Large kiosk-style buttons - reduced size to fit all 5
        buttons_frame = tk.Frame(content_frame, bg="#2a2a2a")
        buttons_frame.pack(pady=10)
        
        # Menu buttons - large and touch-friendly
        buttons = [
            ("MEMBERSHIP PLANS", self.show_membership_plans, "#3498db"),
            ("OPTIONAL EXTRAS", self.show_optional_extras, "#9b59b6"),
            ("KIDS' READING CHALLENGE", self.show_reading_challenge, "#e74c3c"),
            ("RENTAL CALCULATOR", self.show_rental_calculator, "#f39c12"),
            ("EXIT", self.exit_application, "#95a5a6")
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                font=('Arial', 14, 'bold'),
                bg=color,
                fg="white",
                activebackground=color,
                width=35,
                height=2,
                relief=tk.RAISED,
                borderwidth=3,
                cursor="hand2"
            )
            btn.pack(pady=8)
        
        # Right side - Receipt display
        self.create_receipt_display(main_container)
    
    def show_membership_plans(self):
        """Display membership plans menu - Kiosk style."""
        self.clear_frame()
        
        # Create navigation bar FIRST so it's at the bottom
        self.create_navigation_bar()
        
        # Main container - fill remaining space above nav bar
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Selection area
        selection_area = tk.Frame(main_container, bg="#2a2a2a")
        selection_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = tk.Frame(selection_area, bg="#3498db", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="MEMBERSHIP PLANS",
            font=('Arial', 28, 'bold'),
            bg="#3498db",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Content frame - NO SCROLLBAR, fit all on one screen
        content_frame = tk.Frame(selection_area, bg="#2a2a2a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = tk.Label(
            content_frame,
            text="SELECT A MEMBERSHIP PLAN",
            font=('Arial', 16, 'bold'),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        instructions.pack(pady=15)
        
        # Plan buttons - reduced spacing to fit all on screen
        plans_frame = tk.Frame(content_frame, bg="#2a2a2a")
        plans_frame.pack(pady=10)
        
        plans = [
            ("STANDARD", "STANDARD", STANDARD_MONTHLY, "#27ae60"),
            ("PREMIUM", "PREMIUM", PREMIUM_MONTHLY, "#e74c3c"),
            ("KIDS", "KIDS", KIDS_MONTHLY, "#f39c12")
        ]
        
        for name, plan_type, monthly_cost, color in plans:
            plan_frame = tk.Frame(plans_frame, bg="#2a2a2a")
            plan_frame.pack(pady=8)  # Reduced from 15 to 8
            
            btn = tk.Button(
                plan_frame,
                text=f"{name}\n{format_currency(monthly_cost)}/month",
                command=lambda pt=plan_type, n=name, c=monthly_cost: self.show_plan_details(pt, n, c),
                font=('Arial', 16, 'bold'),  # Reduced from 18 to 16
                bg=color,
                fg="white",
                activebackground=color,
                width=38,  # Reduced from 40
                height=2,  # Reduced from 3
                relief=tk.RAISED,
                borderwidth=3,
                cursor="hand2"
            )
            btn.pack()
        
        # Right side - Receipt display
        self.create_receipt_display(main_container)
    
    def show_plan_details(self, plan_type: str, name: str, monthly_cost: float):
        """Show detailed membership plan information before adding to cart."""
        plan_info = {
            'STANDARD': {
                'description': 'Basic membership with access to library facilities.'
            },
            'PREMIUM': {
                'description': 'Includes all standard features plus book discounts and special sales.'
            },
            'KIDS': {
                'description': 'Same as standard membership but only for members 12 or younger.'
            }
        }
        
        description = plan_info[plan_type]['description']
        annual_cost = monthly_cost * ANNUAL_DISCOUNT_MONTHS
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"{name} Membership Plan")
        details_window.geometry("500x400")
        details_window.configure(bg="#1a1a1a")
        
        # Title
        title_frame = tk.Frame(details_window, bg="#3498db", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text=f"{name} MEMBERSHIP PLAN",
            font=('Arial', 20, 'bold'),
            bg="#3498db",
            fg="white"
        )
        title_label.pack(pady=25)
        
        # Details frame
        details_frame = tk.Frame(details_window, bg="#2a2a2a")
        details_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Plan information
        info_text = f"Plan Name: {name}\n\n"
        info_text += f"Monthly Cost: {format_currency(monthly_cost)}\n"
        info_text += f"Annual Cost: {format_currency(annual_cost)} (11 months - 1 month free!)\n\n"
        info_text += f"Description:\n{description}"
        
        info_label = tk.Label(
            details_frame,
            text=info_text,
            font=('Arial', 12),
            bg="#2a2a2a",
            fg="#ffffff",
            justify=tk.LEFT,
            anchor="w"
        )
        info_label.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(details_frame, bg="#2a2a2a")
        buttons_frame.pack(pady=20)
        
        # Add to cart button
        add_btn = tk.Button(
            buttons_frame,
            text="ADD TO CART",
            command=lambda: self.add_membership_and_close(plan_type, name, monthly_cost, details_window),
            font=('Arial', 12, 'bold'),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        add_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(
            buttons_frame,
            text="CLOSE",
            command=details_window.destroy,
            font=('Arial', 12, 'bold'),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def add_membership_and_close(self, plan_type: str, name: str, cost: float, window):
        """Add membership to cart and close details window."""
        self.cart['membership'] = {
            'type': plan_type,
            'name': name,
            'cost': cost
        }
        self.update_receipt_display()
        window.destroy()
        messagebox.showinfo("Added", f"{name} membership added to cart!")
    
    def add_membership_to_cart(self, plan_type: str, name: str, cost: float):
        """Add membership to cart."""
        self.cart['membership'] = {
            'type': plan_type,
            'name': name,
            'cost': cost
        }
        self.update_receipt_display()
        messagebox.showinfo("Added", f"{name} membership added to cart!")
    
    def show_optional_extras(self):
        """Display optional extras selection interface - Kiosk style."""
        self.clear_frame()
        
        # Create navigation bar FIRST
        self.create_navigation_bar()
        
        # Main container - leave space for nav bar at bottom
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 90))
        
        # Left side - Selection area
        selection_area = tk.Frame(main_container, bg="#2a2a2a")
        selection_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = tk.Frame(selection_area, bg="#9b59b6", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="OPTIONAL EXTRAS",
            font=('Arial', 28, 'bold'),
            bg="#9b59b6",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Scrollable content
        canvas = tk.Canvas(selection_area, bg="#2a2a2a", highlightthickness=0)
        scrollbar = ttk.Scrollbar(selection_area, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2a2a2a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Extras information
        extras_info = [
            ("BOOK RENTAL", EXTRA_BOOK_RENTAL_COST,
             "Borrow older books, one at a time, up to twice per month, separate from Aurora-Picks.", "#3498db"),
            ("PRIVATE AREA ACCESS", EXTRA_PRIVATE_AREA_COST,
             "Quiet reading area on second floor.", "#27ae60"),
            ("MONTHLY BOOKLET", EXTRA_MONTHLY_BOOKLET_COST,
             "Booklet with news, events, reviews, and upcoming releases.", "#e74c3c"),
            ("ONLINE EBOOK RENTAL", EXTRA_ONLINE_EBOOK_RENTAL_COST,
             "E-reader access, 7-day automatic returns, one member at a time.", "#f39c12")
        ]
        
        # Instructions
        instructions = tk.Label(
            scrollable_frame,
            text="SELECT OPTIONAL EXTRAS",
            font=('Arial', 16, 'bold'),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        instructions.pack(pady=20, padx=20)
        
        # Checkboxes for extras
        self.extras_vars = {}
        extras_frame = tk.Frame(scrollable_frame, bg="#2a2a2a")
        extras_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        for name, cost, description, color in extras_info:
            # Check if already in cart
            in_cart = any(extra['name'] == name for extra in self.cart['extras'])
            
            frame = tk.Frame(extras_frame, bg="#3a3a3a", relief=tk.RAISED, borderwidth=2)
            frame.pack(fill=tk.X, pady=10, padx=10)
            
            var = tk.BooleanVar(value=in_cart)
            self.extras_vars[name] = var
            
            # Button-style checkbox
            checkbox_frame = tk.Frame(frame, bg="#3a3a3a")
            checkbox_frame.pack(fill=tk.X, padx=10, pady=10)
            
            checkbox = tk.Checkbutton(
                checkbox_frame,
                text=f"{name} - {format_currency(cost)}/month",
                variable=var,
                font=('Arial', 14, 'bold'),
                bg="#3a3a3a",
                fg="white",
                activebackground="#3a3a3a",
                selectcolor="#2a2a2a",
                command=lambda n=name, c=cost, v=var: self.update_extra_in_cart(n, c, v)
            )
            checkbox.pack(anchor="w")
            
            desc_label = tk.Label(
                checkbox_frame,
                text=description,
                font=('Arial', 10),
                bg="#3a3a3a",
                fg="#cccccc",
                justify=tk.LEFT,
                anchor="w"
            )
            desc_label.pack(anchor="w", padx=30, pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Right side - Receipt display
        self.create_receipt_display(main_container)
    
    def update_extra_in_cart(self, name: str, cost: float, var: tk.BooleanVar):
        """Add or remove extra from cart based on checkbox state."""
        if var.get():
            # Add to cart if not already there
            if not any(extra['name'] == name for extra in self.cart['extras']):
                self.cart['extras'].append({'name': name, 'cost': cost})
        else:
            # Remove from cart
            self.cart['extras'] = [e for e in self.cart['extras'] if e['name'] != name]
        
        self.update_receipt_display()
    
    def show_reading_challenge(self):
        """Display Kids' Reading Challenge interface - Kiosk style."""
        self.clear_frame()
        
        # Create navigation bar FIRST
        self.create_navigation_bar()
        
        # Main container - leave space for nav bar at bottom
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 90))
        
        # Left side - Input area
        input_area = tk.Frame(main_container, bg="#2a2a2a")
        input_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = tk.Frame(input_area, bg="#e74c3c", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="KIDS' READING CHALLENGE",
            font=('Arial', 28, 'bold'),
            bg="#e74c3c",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Content frame
        content_frame = tk.Frame(input_area, bg="#2a2a2a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Instructions
        instructions = tk.Label(
            content_frame,
            text="ENTER PAGES READ FOR EACH WEEKDAY",
            font=('Arial', 16, 'bold'),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        instructions.pack(pady=20)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg="#2a2a2a")
        input_frame.pack(pady=30)
        
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.pages_entries = {}
        
        for day in weekdays:
            row_frame = tk.Frame(input_frame, bg="#2a2a2a")
            row_frame.pack(pady=10)
            
            label = tk.Label(
                row_frame,
                text=f"{day.upper()}:",
                font=('Arial', 14, 'bold'),
                bg="#2a2a2a",
                fg="#ffffff",
                width=15,
                anchor="e"
            )
            label.pack(side=tk.LEFT, padx=10)
            
            entry = tk.Entry(
                row_frame,
                font=('Arial', 16),
                width=20,
                bg="#ffffff",
                fg="#000000"
            )
            entry.pack(side=tk.LEFT, padx=10)
            self.pages_entries[day] = entry
        
        # Calculate button
        calc_btn = tk.Button(
            content_frame,
            text="CALCULATE RESULTS",
            command=self.calculate_reading_challenge,
            font=('Arial', 16, 'bold'),
            bg="#9b59b6",
            fg="white",
            activebackground="#8e44ad",
            width=35,
            height=3,
            relief=tk.RAISED,
            cursor="hand2"
        )
        calc_btn.pack(pady=30)
        
        # Right side - Receipt display
        self.create_receipt_display(main_container)
    
    def calculate_reading_challenge(self):
        """Calculate and display reading challenge results."""
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        pages_read = {}
        
        # Validate and collect input
        try:
            for day in weekdays:
                value = self.pages_entries[day].get().strip()
                if value == "":
                    messagebox.showerror("Error", f"Please enter pages read for {day}.")
                    return
                pages_read[day] = float(value)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for all days.")
            return
        
        # Calculate totals and averages
        total_pages = sum(pages_read.values())
        average_pages = total_pages / len(weekdays)
        
        # Determine rank
        if total_pages <= RANK_THRESHOLD_BRONZE_MAX:
            rank = "Bronze"
            next_rank = "Silver"
            pages_to_next = max(0.01, RANK_THRESHOLD_BRONZE_MAX + 0.01 - total_pages)
        elif total_pages <= RANK_THRESHOLD_SILVER_MAX:
            rank = "Silver"
            next_rank = "Gold"
            pages_to_next = max(0.01, RANK_THRESHOLD_SILVER_MAX + 0.01 - total_pages)
        elif total_pages <= RANK_THRESHOLD_GOLD_MAX:
            rank = "Gold"
            next_rank = "Platinum"
            pages_to_next = max(0.01, RANK_THRESHOLD_GOLD_MAX + 0.01 - total_pages)
        else:
            rank = "Platinum"
            next_rank = None
            pages_to_next = 0
        
        # Find best day(s)
        max_pages = max(pages_read.values())
        best_days = [day for day, pages in pages_read.items() if pages == max_pages]
        
        # Check for record breaking
        record_broken = total_pages > READING_CHALLENGE_WEEKLY_RECORD
        
        # Store in cart (for tracking, no cost)
        self.cart['reading_challenge'] = {
            'pages_read': pages_read,
            'total': total_pages,
            'rank': rank
        }
        
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Reading Challenge Results")
        results_window.geometry("700x700")
        results_window.configure(bg="#1a1a1a")
        
        # Title
        title_frame = tk.Frame(results_window, bg="#e74c3c", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="READING CHALLENGE RESULTS",
            font=('Arial', 22, 'bold'),
            bg="#e74c3c",
            fg="white"
        )
        title_label.pack(pady=20)
        
        # Results frame with scrollbar
        canvas = tk.Canvas(results_window, bg="#2a2a2a")
        scrollbar = ttk.Scrollbar(results_window, orient="vertical", command=canvas.yview)
        results_frame = tk.Frame(canvas, bg="#2a2a2a")
        
        results_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=results_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Weekly summary
        summary_text = "WEEKLY READING SUMMARY\n" + "─" * 50 + "\n"
        for day in weekdays:
            summary_text += f"{day:12} : {pages_read[day]:6.2f} pages\n"
        summary_text += "─" * 50 + "\n\n"
        summary_text += f"Total Pages Read: {total_pages:.2f} pages\n"
        summary_text += f"Average Pages Per Day: {average_pages:.2f} pages\n\n"
        
        summary_label = tk.Label(
            results_frame,
            text=summary_text,
            font=('Courier', 12),
            bg="#2a2a2a",
            fg="#00ff00",
            justify=tk.LEFT,
            anchor="w"
        )
        summary_label.pack(pady=20, padx=30)
        
        # Ranking
        rank_text = "RANKING\n" + "─" * 50 + "\n"
        rank_text += f"Current Rank: {rank}\n"
        if next_rank:
            rank_text += f"Pages Needed for {next_rank}: {pages_to_next:.2f} pages\n"
        else:
            rank_text += "You're already at the highest rank!\n"
        rank_text += "─" * 50 + "\n\n"
        
        rank_label = tk.Label(
            results_frame,
            text=rank_text,
            font=('Courier', 12),
            bg="#2a2a2a",
            fg="#00ff00",
            justify=tk.LEFT,
            anchor="w"
        )
        rank_label.pack(pady=10, padx=30)
        
        # Best day(s)
        if len(best_days) == 1:
            best_text = f"{best_days[0]} was your biggest reading day!"
        else:
            best_text = f"{', '.join(best_days)} were your biggest reading day(s)!"
        
        best_label = tk.Label(
            results_frame,
            text=best_text,
            font=('Arial', 12, 'bold'),
            bg="#2a2a2a",
            fg="#ffff00"
        )
        best_label.pack(pady=10, padx=30)
        
        # Record breaking
        if record_broken:
            record_text = f"\n🎉 CONGRATULATIONS! 🎉\n\n"
            record_text += f"You've broken the weekly record of {READING_CHALLENGE_WEEKLY_RECORD} pages!\n"
            record_text += f"Your total of {total_pages:.2f} pages is amazing!"
            
            record_label = tk.Label(
                results_frame,
                text=record_text,
                font=('Arial', 14, 'bold'),
                bg="#2a2a2a",
                fg="#ff0000",
                justify=tk.CENTER
            )
            record_label.pack(pady=20, padx=30)
        
        # Close button
        close_btn = tk.Button(
            results_frame,
            text="CLOSE",
            command=results_window.destroy,
            font=('Arial', 12, 'bold'),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_btn.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def show_rental_calculator(self):
        """Display Aurora-Picks Rental Calculator interface - Kiosk style."""
        self.clear_frame()
        
        # Create navigation bar FIRST
        self.create_navigation_bar()
        
        # Main container - leave space for nav bar at bottom
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 90))
        
        # Left side - Input area
        input_area = tk.Frame(main_container, bg="#2a2a2a")
        input_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title bar
        title_frame = tk.Frame(input_area, bg="#f39c12", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="AURORA-PICKS RENTAL",
            font=('Arial', 28, 'bold'),
            bg="#f39c12",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Content frame
        content_frame = tk.Frame(input_area, bg="#2a2a2a")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Description
        desc_label = tk.Label(
            content_frame,
            text="Aurora-Picks: Special hand-picked rentals\nChoose from our curated selection of premium books.",
            font=('Arial', 14),
            bg="#2a2a2a",
            fg="#ffffff",
            justify=tk.CENTER
        )
        desc_label.pack(pady=30)
        
        # Input frame
        input_frame = tk.Frame(content_frame, bg="#2a2a2a")
        input_frame.pack(pady=40)
        
        days_label = tk.Label(
            input_frame,
            text="ENTER NUMBER OF DAYS TO RENT:",
            font=('Arial', 16, 'bold'),
            bg="#2a2a2a",
            fg="#ffffff"
        )
        days_label.pack(pady=20)
        
        self.days_entry = tk.Entry(
            input_frame,
            font=('Arial', 20),
            width=15,
            bg="#ffffff",
            fg="#000000",
            justify=tk.CENTER
        )
        self.days_entry.pack(pady=20)
        
        # Info label
        info_text = f"Minimum: {RENTAL_MIN_DAYS} days | Maximum: {RENTAL_MAX_DAYS} days"
        info_label = tk.Label(
            input_frame,
            text=info_text,
            font=('Arial', 12),
            bg="#2a2a2a",
            fg="#cccccc"
        )
        info_label.pack(pady=10)
        
        # Calculate button
        calc_btn = tk.Button(
            content_frame,
            text="CALCULATE & ADD TO CART",
            command=self.calculate_and_add_rental,
            font=('Arial', 16, 'bold'),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            width=35,
            height=3,
            relief=tk.RAISED,
            cursor="hand2"
        )
        calc_btn.pack(pady=30)
        
        # Right side - Receipt display
        self.create_receipt_display(main_container)
    
    def calculate_and_add_rental(self):
        """Calculate rental cost and add to cart."""
        try:
            days = int(self.days_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of days.")
            return
        
        # Validate days
        if days < RENTAL_MIN_DAYS:
            messagebox.showerror(
                "Error",
                f"Minimum rental period is {RENTAL_MIN_DAYS} days."
            )
            return
        elif days > RENTAL_MAX_DAYS:
            messagebox.showerror(
                "Error",
                f"Maximum rental period is {RENTAL_MAX_DAYS} days."
            )
            return
        
        # Calculate cost
        if days == 21:
            total_cost = RENTAL_FIXED_COST_21_DAYS
        else:
            total_cost = 0.00
            
            if days >= 3:
                total_cost += 3 * RENTAL_RATE_DAYS_1_3
            else:
                total_cost += days * RENTAL_RATE_DAYS_1_3
            
            if days > 3:
                days_4_to_8 = min(5, days - 3)
                total_cost += days_4_to_8 * RENTAL_RATE_DAYS_4_8
            
            if days > 8:
                days_9_plus = days - 8
                total_cost += days_9_plus * RENTAL_RATE_DAYS_9_PLUS
        
        # Add to cart
        self.cart['rental'] = {
            'days': days,
            'cost': total_cost
        }
        
        self.update_receipt_display()
        messagebox.showinfo("Added", f"Rental ({days} days) added to cart!\nCost: {format_currency(total_cost)}")
    
    def show_cart(self):
        """Show detailed cart view."""
        cart_window = tk.Toplevel(self.root)
        cart_window.title("Shopping Cart")
        cart_window.geometry("600x600")
        cart_window.configure(bg="#1a1a1a")
        
        # Title
        title_frame = tk.Frame(cart_window, bg="#ff6600", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="SHOPPING CART",
            font=('Arial', 24, 'bold'),
            bg="#ff6600",
            fg="white"
        )
        title_label.pack(pady=25)
        
        # Cart content
        cart_frame = tk.Frame(cart_window, bg="#2a2a2a")
        cart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        total = 0.00
        cart_text = ""
        
        # Membership
        if self.cart['membership']:
            membership = self.cart['membership']
            cart_text += f"Membership: {membership['name']}\n"
            cart_text += f"  {format_currency(membership['cost'])}/month\n\n"
            total += membership['cost']
        
        # Extras
        if self.cart['extras']:
            cart_text += "Extras:\n"
            for extra in self.cart['extras']:
                cart_text += f"  {extra['name']}: {format_currency(extra['cost'])}/month\n"
                total += extra['cost']
            cart_text += "\n"
        
        # Rental
        if self.cart['rental']:
            rental = self.cart['rental']
            cart_text += f"Rental: {rental['days']} days\n"
            cart_text += f"  {format_currency(rental['cost'])}\n\n"
            total += rental['cost']
        
        if total == 0.00:
            cart_text = "Cart is empty"
        
        cart_text += "\n" + "=" * 40 + "\n"
        cart_text += f"TOTAL: {format_currency(total)}"
        
        cart_label = tk.Label(
            cart_frame,
            text=cart_text,
            font=('Courier', 12),
            bg="#2a2a2a",
            fg="#00ff00",
            justify=tk.LEFT,
            anchor="w"
        )
        cart_label.pack(pady=20, padx=20)
        
        # Close button
        close_btn = tk.Button(
            cart_frame,
            text="CLOSE",
            command=cart_window.destroy,
            font=('Arial', 12, 'bold'),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_btn.pack(pady=20)
    
    def show_checkout(self):
        """Show final checkout with total."""
        # Calculate total
        total = 0.00
        
        if self.cart['membership']:
            total += self.cart['membership']['cost']
        
        for extra in self.cart['extras']:
            total += extra['cost']
        
        if self.cart['rental']:
            total += self.cart['rental']['cost']
        
        if total == 0.00:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Please add items before checkout.")
            return
        
        # Create checkout window
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Checkout")
        checkout_window.geometry("700x700")
        checkout_window.configure(bg="#1a1a1a")
        
        # Title
        title_frame = tk.Frame(checkout_window, bg="#00aa00", height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="CHECKOUT",
            font=('Arial', 28, 'bold'),
            bg="#00aa00",
            fg="white"
        )
        title_label.pack(pady=30)
        
        # Receipt frame
        receipt_frame = tk.Frame(checkout_window, bg="#000000", relief=tk.RAISED, borderwidth=3)
        receipt_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        # Receipt content
        receipt_text = scrolledtext.ScrolledText(
            receipt_frame,
            font=('Courier', 11),
            bg="#000000",
            fg="#00ff00",
            wrap=tk.WORD,
            relief=tk.FLAT,
            borderwidth=0
        )
        receipt_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Build receipt
        receipt_lines = []
        receipt_lines.append(" " * 20 + "LIBRARY KIOSK\n")
        receipt_lines.append(" " * 20 + "═══════════════\n")
        receipt_lines.append(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        receipt_lines.append(" " * 20 + "═══════════════\n\n")
        
        # Membership
        if self.cart['membership']:
            membership = self.cart['membership']
            receipt_lines.append(f"Membership Plan:\n")
            receipt_lines.append(f"  {membership['name']}\n")
            receipt_lines.append(f"  {format_currency(membership['cost'])}/month\n\n")
        
        # Extras
        if self.cart['extras']:
            receipt_lines.append("Optional Extras:\n")
            for extra in self.cart['extras']:
                receipt_lines.append(f"  {extra['name']}\n")
                receipt_lines.append(f"  {format_currency(extra['cost'])}/month\n")
            receipt_lines.append("\n")
        
        # Rental
        if self.cart['rental']:
            rental = self.cart['rental']
            receipt_lines.append("Rental:\n")
            receipt_lines.append(f"  {rental['days']} days\n")
            receipt_lines.append(f"  {format_currency(rental['cost'])}\n\n")
        
        receipt_lines.append(" " * 20 + "═══════════════\n")
        receipt_lines.append(f"\n{'TOTAL:':>30} {format_currency(total):>15}\n")
        receipt_lines.append(" " * 20 + "═══════════════\n\n")
        receipt_lines.append(" " * 15 + "THANK YOU!\n")
        receipt_lines.append(" " * 12 + "Have a great day!\n")
        
        receipt_text.insert(1.0, "".join(receipt_lines))
        receipt_text.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = tk.Frame(checkout_window, bg="#1a1a1a")
        buttons_frame.pack(pady=20)
        
        # Print button (simulated)
        print_btn = tk.Button(
            buttons_frame,
            text="PRINT RECEIPT",
            command=lambda: messagebox.showinfo("Print", "Receipt printed!"),
            font=('Arial', 12, 'bold'),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        print_btn.pack(side=tk.LEFT, padx=10)
        
        # New order button
        new_order_btn = tk.Button(
            buttons_frame,
            text="NEW ORDER",
            command=lambda: self.new_order(checkout_window),
            font=('Arial', 12, 'bold'),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        new_order_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(
            buttons_frame,
            text="CLOSE",
            command=checkout_window.destroy,
            font=('Arial', 12, 'bold'),
            bg="#95a5a6",
            fg="white",
            activebackground="#7f8c8d",
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor="hand2"
        )
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def new_order(self, window):
        """Clear cart and start new order."""
        self.cart = {
            'membership': None,
            'extras': [],
            'rental': None,
            'reading_challenge': None
        }
        window.destroy()
        self.create_main_menu()
        messagebox.showinfo("New Order", "Cart cleared. Ready for new order!")
    
    def exit_application(self):
        """Exit the application with confirmation."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()


def main():
    """Main function - entry point of the GUI application."""
    root = tk.Tk()
    app = LibraryManagementGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
