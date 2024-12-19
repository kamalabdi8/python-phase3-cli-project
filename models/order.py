from database.connection import get_db_connection

class Order:
    def __init__(self, id, description, quantity, customer_id, restaurant_id):
        self.id = id
        self.description = description
        self.quantity = quantity
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f'<Order {self.description}>'

    def customer(self):
        from models.customer import Customer
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (self.customer_id,))
        customer = cursor.fetchone()
        conn.close()
        return Customer(customer['id'], customer['name'], customer['email']) if customer else None

    def restaurant(self):
        from models.restaurant import Restaurant
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants WHERE id = ?', (self.restaurant_id,))
        restaurant = cursor.fetchone()
        conn.close()
        return Restaurant(restaurant['id'], restaurant['name'], restaurant['location']) if restaurant else None

    @classmethod
    def create_order(cls, description, quantity, customer_id, restaurant_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO orders (description, quantity, customer_id, restaurant_id) VALUES (?, ?, ?, ?)',
                       (description, quantity, customer_id, restaurant_id))
        conn.commit()
        conn.close()
        return cls(cursor.lastrowid, description, quantity, customer_id, restaurant_id)

    def update_order(self, description=None, quantity=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if description:
            cursor.execute('UPDATE orders SET description = ? WHERE id = ?', (description, self.id))
            self.description = description
        if quantity:
            cursor.execute('UPDATE orders SET quantity = ? WHERE id = ?', (quantity, self.id))
            self.quantity = quantity
        conn.commit()
        conn.close()

    def delete_order(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
