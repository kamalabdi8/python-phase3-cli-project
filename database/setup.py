from .connection import get_db_connection

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            order_quantity INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            restaurant_id INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (restaurant_id) REFERENCES restaurants (id)
        )
    ''')

    conn.commit()
    conn.close()
