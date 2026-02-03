import sqlite3

# ==================================================
# Section 1 – Summaries
# ==================================================

def total_customers(conn):
    """Display the total number of customers."""
    query = "SELECT COUNT(*) FROM customers;"
    cursor = conn.execute(query)
    result = cursor.fetchone()
    
    print("\n" + "="*50)
    print("TOTAL CUSTOMERS")
    print("="*50)
    print(f"Total number of customers: {result[0]}")
    print()



def customer_signup_range(conn):
    """Show the earliest and latest customer signup dates."""
    query = """
    SELECT 
        MIN(signup_date) AS earliest,
        MAX(signup_date) AS latest
    FROM customers;
    """
    cursor = conn.execute(query)
    result = cursor.fetchone()
    
    print("\n" + "="*50)
    print("CUSTOMER SIGNUP DATE RANGE")
    print("="*50)
    print(f"Earliest signup: {result['earliest']}")
    print(f"Latest signup:   {result['latest']}")
    print()



def order_summary_stats(conn):
    """
    Display:
    - total number of orders
    - average order value
    - highest and lowest order totals
    """
    query = """
    SELECT 
        COUNT(*) AS total_orders,
        ROUND(AVG(order_total), 2) AS avg_value,
        MAX(order_total) AS highest,
        MIN(order_total) AS lowest
    FROM orders;
    """
    cursor = conn.execute(query)
    result = cursor.fetchone()
    
    print("\n" + "="*50)
    print("ORDER SUMMARY STATISTICS")
    print("="*50)
    print(f"Total orders:        {result['total_orders']}")
    print(f"Average order value: £{result['avg_value']:.2f}")
    print(f"Highest order:       £{result['highest']:.2f}")
    print(f"Lowest order:        £{result['lowest']:.2f}")
    print()


def driver_summary(conn):
    """Display the total number of drivers and their hire date range."""
    query = """
    SELECT 
        COUNT(*) AS total_drivers,
        MIN(hire_date) AS earliest_hire,
        MAX(hire_date) AS latest_hire
    FROM drivers;
    """
    cursor = conn.execute(query)
    result = cursor.fetchone()
    
    print("\n" + "="*50)
    print("DRIVER SUMMARY")
    print("="*50)
    print(f"Total drivers:   {result['total_drivers']}")
    print(f"Earliest hire:   {result['earliest_hire']}")
    print(f"Latest hire:     {result['latest_hire']}")
    print()


# ==================================================
# Section 2 – Key Statistics
# ==================================================

def orders_per_customer(conn):
    """
    Display orders per customer:
    - Customer name
    - Number of orders
    - Total amount spent
    """
    query = """
    SELECT 
        c.customer_name,
        COUNT(o.order_id) AS num_orders,
        ROUND(IFNULL(SUM(o.order_total), 0), 2) AS total_spent
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC;
    """
    cursor = conn.execute(query)
    
    print("\n" + "="*70)
    print("ORDERS PER CUSTOMER")
    print("="*70)
    print(f"{'Customer Name':<35} | {'Orders':>8} | {'Total Spent':>12}")
    print("-"*70)
    
    for row in cursor:
        print(f"{row['customer_name']:<35} | {row['num_orders']:>8} | £{row['total_spent']:>10.2f}")
    print()


def driver_workload(conn):
    """
    Display driver workload:
    - Driver name
    - Number of deliveries completed
    """
    query = """
    SELECT 
        dr.driver_name,
        COUNT(del.delivery_id) AS deliveries_completed
    FROM drivers dr
    LEFT JOIN deliveries del ON dr.driver_id = del.driver_id
    GROUP BY dr.driver_id, dr.driver_name
    ORDER BY deliveries_completed DESC;
    """
    cursor = conn.execute(query)
    
    print("\n" + "="*60)
    print("DRIVER WORKLOAD")
    print("="*60)
    print(f"{'Driver Name':<40} | {'Deliveries':>12}")
    print("-"*60)
    
    for row in cursor:
        print(f"{row['driver_name']:<40} | {row['deliveries_completed']:>12}")
    print()


def delivery_lookup_by_id(conn, order_id):
    """
    Search for an individual order by ID and display:
    - customer name
    - order total
    - delivery date
    - driver
    """
    query = """
    SELECT 
        o.order_id,
        c.customer_name,
        o.order_total,
        o.order_date,
        del.delivery_date,
        dr.driver_name
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    LEFT JOIN deliveries del ON o.order_id = del.order_id
    LEFT JOIN drivers dr ON del.driver_id = dr.driver_id
    WHERE o.order_id = ?;
    """
    cursor = conn.execute(query, (order_id,))
    result = cursor.fetchone()
    
    print("\n" + "="*60)
    print(f"ORDER LOOKUP - ID: {order_id}")
    print("="*60)
    
    if result:
        print(f"Customer:      {result['customer_name']}")
        print(f"Order Total:   £{result['order_total']:.2f}")
        print(f"Order Date:    {result['order_date']}")
        
        if result['delivery_date']:
            print(f"Delivery Date: {result['delivery_date']}")
            print(f"Driver:        {result['driver_name']}")
        else:
            print("Delivery Date: Not yet delivered")
            print("Driver:        N/A")
    else:
        print(f"Order ID {order_id} not found.")
    print()


# ==================================================
# Section 3 – Time-based Summaries
# ==================================================

def orders_per_date(conn):
    """Count the number of orders per order date."""
    query = """
    SELECT 
        order_date,
        COUNT(*) AS num_orders
    FROM orders
    GROUP BY order_date
    ORDER BY order_date;
    """
    cursor = conn.execute(query)
    
    print("\n" + "="*50)
    print("ORDERS PER DATE")
    print("="*50)
    print(f"{'Date':<15} | {'Number of Orders':>15}")
    print("-"*50)
    
    for row in cursor:
        print(f"{row['order_date']:<15} | {row['num_orders']:>15}")
    print()


def deliveries_per_date(conn):
    """Count the number of deliveries per delivery date."""
    query = """
    SELECT 
        delivery_date,
        COUNT(*) AS num_deliveries
    FROM deliveries
    GROUP BY delivery_date
    ORDER BY delivery_date;
    """
    cursor = conn.execute(query)
    
    print("\n" + "="*50)
    print("DELIVERIES PER DATE")
    print("="*50)
    print(f"{'Date':<15} | {'Number of Deliveries':>20}")
    print("-"*50)
    
    for row in cursor:
        print(f"{row['delivery_date']:<15} | {row['num_deliveries']:>20}")
    print()

def customer_signups_per_month(conn):
    """
    Count customer signups per month.
    Uses Python to process the dates into month format.
    """
    query = "SELECT signup_date FROM customers ORDER BY signup_date;"
    cursor = conn.execute(query)
    
    # Dictionary to count signups per month
    monthly_signups = defaultdict(int)
    
    for row in cursor:
        signup_date = row['signup_date']
        # Parse the date and extract year-month
        try:
            date_obj = datetime.strptime(signup_date, '%Y-%m-%d')
            month_key = date_obj.strftime('%Y-%m')  # Format: "2024-03"
            monthly_signups[month_key] += 1
        except ValueError:
            # If date format is different, try alternative parsing
            continue
    
    print("\n" + "="*50)
    print("CUSTOMER SIGNUPS PER MONTH")
    print("="*50)
    print(f"{'Month':<15} | {'Signups':>10}")
    print("-"*50)


# ==================================================
# Section 4 – Performance and Rankings
# ==================================================

def top_customers_by_spend(conn, limit=5):
    """List the top N customers by total spend."""
    query = """
    SELECT 
        c.customer_name,
        ROUND(SUM(o.order_total), 2) AS total_spent
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_spent DESC
    LIMIT ?;
    """
    cursor = conn.execute(query, (limit,))
    
    print("\n" + "="*60)
    print(f"TOP {limit} CUSTOMERS BY TOTAL SPEND")
    print("="*60)
    print(f"{'Rank':<6} | {'Customer Name':<35} | {'Total Spent':>12}")
    print("-"*60)
    
    rank = 1
    for row in cursor:
        print(f"{rank:<6} | {row['customer_name']:<35} | £{row['total_spent']:>10.2f}")
        rank += 1
    print()


def rank_drivers_by_deliveries(conn):
    """Rank drivers by number of deliveries completed."""
    query = """
    SELECT 
        dr.driver_name,
        COUNT(del.delivery_id) AS deliveries_completed
    FROM drivers dr
    LEFT JOIN deliveries del ON dr.driver_id = del.driver_id
    GROUP BY dr.driver_id, dr.driver_name
    ORDER BY deliveries_completed DESC;
    """
    cursor = conn.execute(query)
    
    print("\n" + "="*60)
    print("DRIVERS RANKED BY DELIVERIES")
    print("="*60)
    print(f"{'Rank':<6} | {'Driver Name':<35} | {'Deliveries':>12}")
    print("-"*60)
    
    rank = 1
    for row in cursor:
        print(f"{rank:<6} | {row['driver_name']:<35} | {row['deliveries_completed']:>12}")
        rank += 1
    print()


def high_value_orders(conn, threshold):
    """Display all orders above a specified value threshold."""
    query = """
    SELECT 
        o.order_id,
        c.customer_name,
        o.order_date,
        o.order_total
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_total > ?
    ORDER BY o.order_total DESC;
    """
    cursor = conn.execute(query, (threshold,))
    
    print("\n" + "="*80)
    print(f"HIGH-VALUE ORDERS (Above £{threshold:.2f})")
    print("="*80)
    print(f"{'Order ID':<10} | {'Customer Name':<30} | {'Date':<12} | {'Total':>10}")
    print("-"*80)
    
    count = 0
    for row in cursor:
        print(f"{row['order_id']:<10} | {row['customer_name']:<30} | {row['order_date']:<12} | £{row['order_total']:>8.2f}")
        count += 1
    
    print("-"*80)
    print(f"Total orders found: {count}")
    print()


# ==================================================
# Menus - You should not need to change any code below this point until the stretch tasks.
# ==================================================

def section_1_menu(conn):
    while True:
        print("\nSection 1 – Summaries")
        print("1. Total number of customers")
        print("2. Customer signup date range")
        print("3. Order summary statistics")
        print("4. Driver summary")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            total_customers(conn)
        elif choice == "2":
            customer_signup_range(conn)
        elif choice == "3":
            order_summary_stats(conn)
        elif choice == "4":
            driver_summary(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_2_menu(conn):
    while True:
        print("\nSection 2 – Key Statistics")
        print("1. Orders per customer")
        print("2. Driver workload")
        print("3. Order delivery overview")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_customer(conn)
        elif choice == "2":
            driver_workload(conn)
        elif choice == "3":
            order_id = input("Enter order ID: ").strip()
            if not order_id.isdigit():
                print("Please enter a valid integer order ID.")
                continue
            delivery_lookup_by_id(conn, int(order_id))
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_3_menu(conn):
    while True:
        print("\nSection 3 – Time-based Summaries")
        print("1. Orders per date")
        print("2. Deliveries per date")
        print("3. Customer signups per month")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            orders_per_date(conn)
        elif choice == "2":
            deliveries_per_date(conn)
        elif choice == "3":
            customer_signups_per_month(conn)
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def section_4_menu(conn):
    while True:
        print("\nSection 4 – Performance and Rankings")
        print("1. Top 5 customers by total spend")
        print("2. Rank drivers by deliveries completed")
        print("3. High-value orders")
        print("0. Back to main menu")

        choice = input("Select an option: ")

        if choice == "1":
            top_customers_by_spend(conn)
        elif choice == "2":
            rank_drivers_by_deliveries(conn)
        elif choice == "3":
            try:
                threshold = float(input("Enter order value threshold (£): "))
                high_value_orders(conn, threshold)
            except:
                print("Please enter a valid numerical value.")
        elif choice == "0":
            break
        else:
            print("Invalid option. Please try again.")


def main_menu(conn):
    while True:
        print("\n=== Delivery Service Management Dashboard ===")
        print("1. Section 1 – Summaries")
        print("2. Section 2 – Key Statistics")
        print("3. Section 3 – Time-based Summaries")
        print("4. Section 4 – Performance and Rankings")
        print("0. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            section_1_menu(conn)
        elif choice == "2":
            section_2_menu(conn)
        elif choice == "3":
            section_3_menu(conn)
        elif choice == "4":
            section_4_menu(conn)
        elif choice == "0":
            print("Exiting dashboard.")
            break
        else:
            print("Invalid option. Please try again.")

def get_connection(db_path="food_delivery.db"):
    """
    Establish a connection to the SQLite database.
    Returns a connection object.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == "__main__":
    conn = get_connection()
    main_menu(conn)
    conn.close()