from database.connection import get_db_connection
from models.customer import Customer
from models.restaurant import Restaurant
from models.order import Order

def main():
    customer_name = input("Enter customer's name: ")
    customer_email = input("Enter customer's email: ")
    restaurant_name = input("Enter restaurant name: ")
    restaurant_location = input("Enter restaurant location: ")

    while True:
        try:
            order_quantity = int(input("Enter order quantity: "))
            break
        except ValueError:
            print("Please enter a valid integer for the order quantity.")

    order_description = input("Enter order description: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if order already exists
    cursor.execute('SELECT id FROM orders WHERE description = ?', (order_description,))
    order_exists = cursor.fetchone()

    if order_exists:
        print(f"Order with description '{order_description}' already exists. Skipping insertion.")
    else:
        cursor.execute('INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)', (customer_name, customer_email))
        customer_id = cursor.execute('SELECT id FROM customers WHERE name = ? AND email = ?', (customer_name, customer_email)).fetchone()[0]

        cursor.execute('INSERT OR IGNORE INTO restaurants (name, location) VALUES (?, ?)', (restaurant_name, restaurant_location))
        restaurant_id = cursor.execute('SELECT id FROM restaurants WHERE name = ? AND location = ?', (restaurant_name, restaurant_location)).fetchone()[0]

        cursor.execute('INSERT INTO orders (description, quantity, customer_id, restaurant_id) VALUES (?, ?, ?, ?)',
                       (order_description, order_quantity, customer_id, restaurant_id))
        conn.commit()
        print("Order successfully added!")

    conn.close()

if __name__ == "__main__":
    main()
