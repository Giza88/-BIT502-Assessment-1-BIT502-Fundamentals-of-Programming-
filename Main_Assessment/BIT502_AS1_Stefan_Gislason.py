"""
Course code: BIT502
Assessment: Assessment 1
My full name: Stefan Gislason
My student number: LG-4785366286
"""

# ============================================================================
# CONSTANTS
# ============================================================================

# Membership monthly costs
STANDARD_MONTHLY = 15.00  # Standard membership monthly cost
PREMIUM_MONTHLY = 25.00   # Premium membership monthly cost
KIDS_MONTHLY = 10.00      # Kids membership monthly cost

# Annual discount rule: 1 month free (annual cost = 11 × monthly)
ANNUAL_DISCOUNT_MONTHS = 11  # Number of months to pay for annual membership

# Optional extras
EXTRA_BOOK_RENTAL = "book rental"
EXTRA_PRIVATE_AREA = "private area"
EXTRA_MONTHLY_BOOKLET = "monthly booklet"
EXTRA_ONLINE_EBOOK_RENTAL = "online ebook rental"

# Optional extras monthly costs
EXTRA_BOOK_RENTAL_COST = 5.00      # Book rental monthly cost
EXTRA_PRIVATE_AREA_COST = 15.00   # Private area access monthly cost
EXTRA_MONTHLY_BOOKLET_COST = 2.00 # Monthly booklet monthly cost
EXTRA_ONLINE_EBOOK_RENTAL_COST = 5.00  # Online ebook rental monthly cost

# Reading challenge constants
READING_CHALLENGE_WEEKLY_RECORD = 150  # Pages per week for reading challenge
# Rank threshold values for Kids' Reading Challenge
RANK_THRESHOLD_BRONZE_MAX = 25   # Maximum pages for Bronze rank
RANK_THRESHOLD_SILVER_MAX = 50   # Maximum pages for Silver rank
RANK_THRESHOLD_GOLD_MAX = 100    # Maximum pages for Gold rank
# Platinum rank has no maximum (unlimited)

# Rental calculator constants
RENTAL_RATE_DAYS_1_3 = 1.00      # Daily rate for first 3 days
RENTAL_RATE_DAYS_4_8 = 0.80      # Daily rate for days 4-8
RENTAL_RATE_DAYS_9_PLUS = 0.50   # Daily rate for days 9+
RENTAL_MIN_DAYS = 3              # Minimum rental days
RENTAL_MAX_DAYS = 21             # Maximum rental days
RENTAL_FIXED_COST_21_DAYS = 12.00  # Fixed cost for 21 days rental

# ============================================================================
# TOP-LEVEL STRUCTURE OUTLINE
# ============================================================================
# 
# The application will need:
# 
# MAIN MENU FUNCTIONS:
# - main_menu() - displays and handles the main menu navigation
# 
# SUB-MENU FUNCTIONS:
# - membership_plans_menu() - handles membership plans sub-menu
# 
# FEATURE FLOWS:
# - optional_extras_flow() - handles optional extras selection and processing
# - kids_reading_challenge_flow() - handles Kids' Reading Challenge flow
# - aurora_picks_rental_calculator_flow() - handles Aurora-Picks Rental Calculator flow
# 
# UTILITY FUNCTIONS:
# - clear_console() - clears the console screen
# - validate_menu_input() - validates menu selection input
# - validate_yes_no_input() - validates yes/no input
# - validate_numeric_input() - validates numeric inputs (integers and floats)
# 
# CONSTANTS:
# - [Constants to be defined based on assessment requirements]
# ============================================================================

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def clear_console():
    """Clear the console screen in a cross-platform way (Windows and others)."""
    import os
    import platform
    
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def get_menu_choice(prompt, valid_choices, menu_display_func=None):
    """
    Get and validate menu choice from user with improved UX.
    
    Args:
        prompt (str): The prompt message to display to the user
        valid_choices (list): List of valid choice values (e.g., ['1', '2', '3', '0'])
        menu_display_func (callable, optional): Function to call to re-display menu on invalid input
    
    Returns:
        str: The validated menu choice
    """
    while True:
        choice = input(prompt).strip()
        
        # Check if choice is valid
        if choice in valid_choices:
            return choice
        
        # Handle invalid input with specific error messages
        if choice == "":
            print("\n⚠️  Error: No input provided. Please enter a choice.")
        elif choice.isdigit():
            # It's a number but not in valid choices
            numeric_choices = [c for c in valid_choices if c.isdigit()]
            if numeric_choices:
                min_choice = min(numeric_choices, key=int)
                max_choice = max(numeric_choices, key=int)
                print(f"\n⚠️  Error: '{choice}' is not a valid menu option.")
                print(f"   Please enter a number between {min_choice} and {max_choice}.")
            else:
                print(f"\n⚠️  Error: '{choice}' is not a valid menu option.")
        else:
            # It's not a number (letters, symbols, etc.)
            print(f"\n⚠️  Error: '{choice}' is not a valid choice.")
            print(f"   Please enter a number from the menu options.")
        
        # Re-display menu if function provided
        if menu_display_func:
            print()  # Add spacing
            menu_display_func()
        else:
            # Format valid choices nicely
            sorted_choices = sorted(valid_choices, key=lambda x: (x.isdigit(), int(x) if x.isdigit() else x))
            print(f"   Valid choices are: {', '.join(sorted_choices)}")


def get_yes_no(prompt):
    """
    Get yes/no input from user (case-insensitive).
    
    Args:
        prompt (str): The prompt message to display to the user
    
    Returns:
        bool: True for yes, False for no
    """
    while True:
        response = input(prompt).strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no' (or 'y'/'n').")


def get_float(prompt):
    """
    Get a float value from user input.
    
    Args:
        prompt (str): The prompt message to display to the user
    
    Returns:
        float: The validated float value
    """
    while True:
        try:
            value = input(prompt).strip()
            if value == "":
                print("Input cannot be empty. Please enter a number.")
                continue
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_int(prompt):
    """
    Get an integer value from user input.
    
    Args:
        prompt (str): The prompt message to display to the user
    
    Returns:
        int: The validated integer value
    """
    while True:
        try:
            value = input(prompt).strip()
            if value == "":
                print("Input cannot be empty. Please enter a whole number.")
                continue
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def display_exit_message(message="Thank you for using the system. Goodbye!"):
    """
    Display a clear exit message to the user.
    
    Args:
        message (str): The exit message to display
    """
    print("\n" + "=" * 60)
    print(f"  {message}")
    print("=" * 60 + "\n")


def display_menu_header(title):
    """
    Display a formatted menu header.
    
    Args:
        title (str): The title of the menu
    """
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def format_currency(amount):
    """
    Format a monetary amount with dollar sign and two decimal places.
    
    Args:
        amount (float): The amount to format
    
    Returns:
        str: Formatted currency string (e.g., "$15.00")
    """
    return f"${amount:.2f}"


# ============================================================================
# MEMBERSHIP PLANS FUNCTIONS
# ============================================================================


def show_membership_details(plan_type):
    """
    Display membership plan details including costs and description.
    
    Args:
        plan_type (str): The plan type ('STANDARD', 'PREMIUM', or 'KIDS')
    """
    # Map plan types to their constants and descriptions
    plan_info = {
        'STANDARD': {
            'name': 'Standard',
            'monthly_cost': STANDARD_MONTHLY,
            'description': 'Basic membership with access to library facilities.'
        },
        'PREMIUM': {
            'name': 'Premium',
            'monthly_cost': PREMIUM_MONTHLY,
            'description': 'Includes all standard features plus book discounts and special sales.'
        },
        'KIDS': {
            'name': 'Kids',
            'monthly_cost': KIDS_MONTHLY,
            'description': 'Same as standard membership but only for members 12 or younger.'
        }
    }
    
    # Get plan information
    if plan_type not in plan_info:
        print(f"Error: Unknown plan type '{plan_type}'")
        return
    
    plan = plan_info[plan_type]
    
    # Calculate annual cost (11 months = 1 month free)
    annual_cost = plan['monthly_cost'] * ANNUAL_DISCOUNT_MONTHS
    
    # Display plan details
    print("\n" + "=" * 60)
    print(f"  {plan['name']} Membership Plan")
    print("=" * 60)
    print(f"\nPlan Name: {plan['name']}")
    print(f"Monthly Cost: {format_currency(plan['monthly_cost'])}")
    print(f"Annual Cost: {format_currency(annual_cost)} (11 months - 1 month free!)")
    print(f"\nDescription:")
    print(f"  {plan['description']}")
    print("=" * 60)
    
    # Wait for user to press Enter
    input("\nPress Enter to return to the Membership Plans menu...")
    clear_console()


def membership_plans_menu():
    """
    Display and handle the membership plans sub-menu.
    """
    while True:
        # Clear console and show header
        clear_console()
        display_menu_header("Membership Plans")
        
        # Display menu options
        print("\nPlease select a membership plan:")
        print("  1. Standard")
        print("  2. Premium")
        print("  3. Kids")
        print("  4. Return to main menu")
        print("  5. Exit")
        print("=" * 60)
        
        # Get user choice with menu re-display on error
        def show_menu():
            display_menu_header("Membership Plans")
            print("\nPlease select a membership plan:")
            print("  1. Standard")
            print("  2. Premium")
            print("  3. Kids")
            print("  4. Return to main menu")
            print("  5. Exit")
            print("=" * 60)
        
        choice = get_menu_choice(
            "\nEnter your selection (1-5): ",
            ['1', '2', '3', '4', '5'],
            menu_display_func=show_menu
        )
        
        # Handle user choice
        if choice == '1':
            show_membership_details('STANDARD')
        elif choice == '2':
            show_membership_details('PREMIUM')
        elif choice == '3':
            show_membership_details('KIDS')
        elif choice == '4':
            # Return to main menu
            return
        elif choice == '5':
            # Exit program
            clear_console()
            display_exit_message("Thank you for using the system. Goodbye!")
            exit()


# ============================================================================
# OPTIONAL EXTRAS FUNCTIONS
# ============================================================================


def optional_extras_flow():
    """
    Handle the optional extras selection flow.
    Displays extras information, prompts for selections, and calculates total.
    """
    # Clear console and show header
    clear_console()
    display_menu_header("Optional Extras")
    
    # Display welcome message
    print("\nWelcome! Here are the available optional extras:\n")
    
    # Display each extra with formatted information
    print("=" * 60)
    print("1. Book Rental")
    print(f"   Cost: {format_currency(EXTRA_BOOK_RENTAL_COST)}/month")
    print("   Description: Borrow older books, one at a time, up to twice")
    print("                per month, separate from Aurora-Picks.")
    print()
    
    print("2. Private Area Access")
    print(f"   Cost: {format_currency(EXTRA_PRIVATE_AREA_COST)}/month")
    print("   Description: Quiet reading area on second floor.")
    print()
    
    print("3. Monthly Booklet")
    print(f"   Cost: {format_currency(EXTRA_MONTHLY_BOOKLET_COST)}/month")
    print("   Description: Booklet with news, events, reviews, and")
    print("                upcoming releases.")
    print()
    
    print("4. Online Ebook Rental")
    print(f"   Cost: {format_currency(EXTRA_ONLINE_EBOOK_RENTAL_COST)}/month")
    print("   Description: E-reader access, 7-day automatic returns,")
    print("                one member at a time.")
    print("=" * 60)
    
    # Wait for user to proceed
    print("\nPress Enter to proceed with selection...")
    input()
    
    # Clear console for selection phase
    clear_console()
    display_menu_header("Optional Extras Selection")
    print()
    
    # Prompt yes/no for each extra and store selections
    book_rental_selected = get_yes_no(
        f"Would you like Book Rental for {format_currency(EXTRA_BOOK_RENTAL_COST)} per month (yes/no)? "
    )
    
    private_area_selected = get_yes_no(
        f"Would you like Private Area Access for {format_currency(EXTRA_PRIVATE_AREA_COST)} per month (yes/no)? "
    )
    
    monthly_booklet_selected = get_yes_no(
        f"Would you like Monthly Booklet for {format_currency(EXTRA_MONTHLY_BOOKLET_COST)} per month (yes/no)? "
    )
    
    online_ebook_selected = get_yes_no(
        f"Would you like Online Ebook Rental for {format_currency(EXTRA_ONLINE_EBOOK_RENTAL_COST)} per month (yes/no)? "
    )
    
    # Calculate total monthly cost
    total_cost = 0.00
    selected_extras = []
    
    if book_rental_selected:
        total_cost += EXTRA_BOOK_RENTAL_COST
        selected_extras.append({
            'name': 'Book Rental',
            'cost': EXTRA_BOOK_RENTAL_COST
        })
    
    if private_area_selected:
        total_cost += EXTRA_PRIVATE_AREA_COST
        selected_extras.append({
            'name': 'Private Area Access',
            'cost': EXTRA_PRIVATE_AREA_COST
        })
    
    if monthly_booklet_selected:
        total_cost += EXTRA_MONTHLY_BOOKLET_COST
        selected_extras.append({
            'name': 'Monthly Booklet',
            'cost': EXTRA_MONTHLY_BOOKLET_COST
        })
    
    if online_ebook_selected:
        total_cost += EXTRA_ONLINE_EBOOK_RENTAL_COST
        selected_extras.append({
            'name': 'Online Ebook Rental',
            'cost': EXTRA_ONLINE_EBOOK_RENTAL_COST
        })
    
    # Display summary
    clear_console()
    display_menu_header("Optional Extras Summary")
    print()
    
    if len(selected_extras) == 0:
        print("No extras selected.")
        print(f"\nTotal Monthly Cost: {format_currency(0.00)}")
    else:
        print("Selected Extras:")
        for i, extra in enumerate(selected_extras, 1):
            print(f"  {i}. {extra['name']} - {format_currency(extra['cost'])}/month")
        print(f"\nTotal Monthly Cost: {format_currency(total_cost)}")
    
    print("=" * 60)
    
    # Wait for user before returning to main menu
    input("\nPress Enter to return to the main menu...")
    clear_console()


# ============================================================================
# KIDS' READING CHALLENGE FUNCTIONS
# ============================================================================


def kids_reading_challenge_flow():
    """
    Handle the Kids' Reading Challenge flow.
    Collects pages read per weekday, calculates statistics, determines rank,
    and checks for record breaking.
    """
    # Clear console and show welcome message
    clear_console()
    display_menu_header("Kids' Reading Challenge")
    
    print("\nWelcome to the Kids' Reading Challenge!")
    print("Let's track your reading progress for this week.")
    print("\nHit Enter to start...")
    input()
    
    # Clear console for input phase
    clear_console()
    display_menu_header("Kids' Reading Challenge - Daily Pages")
    print()
    
    # List of weekdays
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    
    # Dictionary to store pages read per day
    pages_read = {}
    
    # Collect pages for each weekday
    for day in weekdays:
        pages = get_float(f"Enter pages read on {day}: ")
        pages_read[day] = pages
    
    # Calculate totals and averages
    total_pages = sum(pages_read.values())
    average_pages = total_pages / len(weekdays)
    
    # Determine rank based on total pages using constants
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
    
    # Find best day(s) - maximum pages and all days with that value
    max_pages = max(pages_read.values())
    best_days = [day for day, pages in pages_read.items() if pages == max_pages]
    
    # Check if record is broken (total > 150)
    record_broken = total_pages > READING_CHALLENGE_WEEKLY_RECORD
    
    # Display results
    clear_console()
    display_menu_header("Kids' Reading Challenge - Results")
    print()
    
    print("Weekly Reading Summary:")
    print("-" * 60)
    for day in weekdays:
        print(f"  {day:12} : {pages_read[day]:6.2f} pages")
    print("-" * 60)
    print(f"\nTotal Pages Read: {total_pages:.2f} pages")
    print(f"Average Pages Per Day: {average_pages:.2f} pages")
    print()
    
    print("Ranking:")
    print("-" * 60)
    print(f"Current Rank: {rank}")
    if next_rank:
        print(f"Pages Needed for {next_rank}: {pages_to_next:.2f} pages")
    else:
        print("You're already at the highest rank!")
    print("-" * 60)
    print()
    
    # Display best day(s)
    if len(best_days) == 1:
        print(f"{best_days[0]} was your biggest reading day!")
    else:
        best_days_str = ", ".join(best_days)
        print(f"{best_days_str} were your biggest reading day(s)!")
    print()
    
    # Check for record breaking
    if record_broken:
        print("=" * 60)
        print("🎉 CONGRATULATIONS! 🎉")
        print(f"You've broken the weekly record of {READING_CHALLENGE_WEEKLY_RECORD} pages!")
        print(f"Your total of {total_pages:.2f} pages is amazing!")
        print("=" * 60)
        print()
    
    # Wait for user before returning to main menu
    input("\nPress Enter to return to the main menu...")
    clear_console()


# ============================================================================
# AURORA-PICKS RENTAL CALCULATOR FUNCTIONS
# ============================================================================


def aurora_picks_calculate_rental():
    """
    Calculate rental cost based on number of days with tiered pricing.
    Handles validation and displays the total cost.
    """
    clear_console()
    display_menu_header("Aurora-Picks Rental Calculator")
    print()
    
    # Get number of days with validation
    while True:
        days = get_int("Enter the number of days to rent: ")
        
        # Validate days are within allowed range
        if days < RENTAL_MIN_DAYS:
            print(f"\n⚠️  Warning: Minimum rental period is {RENTAL_MIN_DAYS} days.")
            print("   Please enter a valid number of days.\n")
            continue
        elif days > RENTAL_MAX_DAYS:
            print(f"\n⚠️  Warning: Maximum rental period is {RENTAL_MAX_DAYS} days.")
            print("   Please enter a valid number of days.\n")
            continue
        else:
            break
    
    # Calculate cost based on rental period
    if days == 21:
        # Fixed cost for 21 days (special promotional rate)
        total_cost = RENTAL_FIXED_COST_21_DAYS
    else:
        # Tiered pricing calculation:
        # - Days 1-3: $1.00/day
        # - Days 4-8: $0.80/day (5 days maximum in this tier)
        # - Days 9+: $0.50/day
        total_cost = 0.00
        
        # First 3 days: base rate
        if days >= 3:
            total_cost += 3 * RENTAL_RATE_DAYS_1_3
        else:
            # Less than 3 days (shouldn't happen due to validation, but handle edge case)
            total_cost += days * RENTAL_RATE_DAYS_1_3
        
        # Days 4 to 8: reduced rate
        if days > 3:
            days_4_to_8 = min(5, days - 3)  # Maximum 5 days (days 4, 5, 6, 7, 8)
            total_cost += days_4_to_8 * RENTAL_RATE_DAYS_4_8
        
        # Days 9+: further reduced rate
        if days > 8:
            days_9_plus = days - 8
            total_cost += days_9_plus * RENTAL_RATE_DAYS_9_PLUS
    
    # Display result
    print("\n" + "=" * 60)
    print("Rental Calculation Result")
    print("=" * 60)
    print(f"\nRental Period: {days} day{'s' if days != 1 else ''}")
    print(f"Total Cost: {format_currency(total_cost)}")
    print("=" * 60)
    
    # Wait for user before returning to menu
    input("\nPress Enter to return to the Aurora-Picks menu...")
    clear_console()


def aurora_picks_menu():
    """
    Display and handle the Aurora-Picks rental calculator sub-menu.
    """
    while True:
        # Clear console and display header
        clear_console()
        display_menu_header("Aurora-Picks Rental Calculator")
        
        # Display description
        print("\nAurora-Picks: Special hand-picked rentals")
        print("Choose from our curated selection of premium books.")
        print()
        print("=" * 60)
        
        # Display menu options
        print("\nOptions:")
        print("  1. Enter rental period")
        print("  2. Return to main menu")
        print("=" * 60)
        
        # Get user choice with menu re-display on error
        def show_menu():
            display_menu_header("Aurora-Picks Rental Calculator")
            print("\nAurora-Picks: Special hand-picked rentals")
            print("Choose from our curated selection of premium books.")
            print()
            print("=" * 60)
            print("\nOptions:")
            print("  1. Enter rental period")
            print("  2. Return to main menu")
            print("=" * 60)
        
        choice = get_menu_choice(
            "\nEnter your selection (1-2): ",
            ['1', '2'],
            menu_display_func=show_menu
        )
        
        # Handle user choice
        if choice == '1':
            # Call calculation function
            aurora_picks_calculate_rental()
            # Function will return here after calculation
        elif choice == '2':
            # Return to main menu
            return


# ============================================================================
# MAIN MENU FUNCTION
# ============================================================================


def main_menu():
    """
    Display and handle the main menu navigation.
    Routes to appropriate sub-menus and features.
    """
    while True:
        # Clear console and show header
        clear_console()
        display_menu_header("Main Menu")
        
        # Display menu options
        print("\nPlease select an option:")
        print("  1. Membership Plans")
        print("  2. Optional Extras")
        print("  3. Kids' Reading Challenge")
        print("  4. Aurora-Picks Rental Calculator")
        print("  5. Exit")
        print("=" * 60)
        
        # Get user choice with menu re-display on error
        def show_menu():
            display_menu_header("Main Menu")
            print("\nPlease select an option:")
            print("  1. Membership Plans")
            print("  2. Optional Extras")
            print("  3. Kids' Reading Challenge")
            print("  4. Aurora-Picks Rental Calculator")
            print("  5. Exit")
            print("=" * 60)
        
        choice = get_menu_choice(
            "\nEnter your selection (1-5): ",
            ['1', '2', '3', '4', '5'],
            menu_display_func=show_menu
        )
        
        # Handle user choice
        if choice == '1':
            membership_plans_menu()
        elif choice == '2':
            optional_extras_flow()
        elif choice == '3':
            kids_reading_challenge_flow()
        elif choice == '4':
            aurora_picks_menu()
        elif choice == '5':
            # Exit program
            clear_console()
            display_exit_message("Thank you for using the system. Goodbye!")
            exit()


def main():
    """Main function - entry point of the application."""
    # Start the main menu loop
    main_menu()


if __name__ == "__main__":
    main()
