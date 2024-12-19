from database.setup import create_tables
from database.connection import get_db_connection
from models.restaurant import Restaurant
from models.customer import Customer
from models.order import Order

def main():
    create_tables()  # Ensure tables are created

    customer_name = input("Enter customer's name: ")
    customer_email = input("Enter customer's email: ")
    restaurant_name = input("Enter restaurant name: ")
    restaurant_location = input("Enter restaurant location: ")

    while True:
        try:
            order_quantity = int(input("Enter order quantity: "))  # Collect quantity input and convert to int
            break  # Exit the loop if conversion is successful
        except ValueError:
            print("Please enter a valid integer for the order quantity.")  # Prompt for valid input

    order_description = input("Enter order description: ")

    customer = Customer.create_customer(customer_name, customer_email)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Insert restaurant if it doesn't exist
    cursor.execute('INSERT OR IGNORE INTO restaurants (name, location) VALUES (?, ?)', (restaurant_name, restaurant_location))
    restaurant_id = cursor.execute('SELECT id FROM restaurants WHERE name = ? AND location = ?', (restaurant_name, restaurant_location)).fetchone()[0]

    # Insert into orders
    cursor.execute('INSERT INTO orders (description, quantity, customer_id, restaurant_id) VALUES (?, ?, ?, ?)',
               (order_description, order_quantity, customer.id, restaurant_id))

    conn.commit()

    cursor.execute('SELECT * FROM restaurants')
    restaurants = cursor.fetchall()

    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()

    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()

    conn.close()

    print("\nRestaurants:")
    for restaurant in restaurants:
        print(Restaurant(restaurant["id"], restaurant["name"], restaurant["location"]))

    print("\nCustomers:")
    for customer in customers:
        print(Customer(customer["id"], customer["name"], customer["email"]))

    print("\nOrders:")
    for order in orders:
        print(Order(order["id"], order["description"], order["quantity"], order["customer_id"], order["restaurant_id"]))

if __name__ == "__main__":
    main()
