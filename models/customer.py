from database.connection import get_db_connection

class Customer:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<Customer {self.name} ({self.email})>'

    def orders(self):
        from models.order import Order
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, description FROM orders WHERE customer_id = ?', (self.id,))
        orders = cursor.fetchall()
        conn.close()
        return [Order(order['id'], order['description'], order['customer_id'], order['restaurant_id']) for order in orders]

    @classmethod
    def create_customer(cls, name, email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        customer_id = cursor.lastrowid
        conn.close()
        return cls(customer_id, name, email)
