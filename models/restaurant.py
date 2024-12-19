from database.connection import get_db_connection

class Restaurant:
    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f'<Restaurant {self.name}>'

    def orders(self):
        from models.order import Order  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE restaurant_id = ?', (self.id,))
        orders = cursor.fetchall()
        conn.close()
        
        if not orders:
            return []
        
        return [Order(order['id'], order['dish_name'], order['quantity'], order['customer_id'], order['restaurant_id']) for order in orders]

    def customers(self):
        from models.customer import Customer  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT customers.* FROM customers
            JOIN orders ON customers.id = orders.customer_id
            WHERE orders.restaurant_id = ?
        ''', (self.id,))
        customers = cursor.fetchall()
        conn.close()
        
        if not customers:
            return []
        
        return [Customer(customer['id'], customer['name'], customer['email']) for customer in customers]

    @classmethod
    def create_restaurant(cls, name, location):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO restaurants (name, location)
            VALUES (?, ?)
        ''', (name, location))
        conn.commit()
        conn.close()
        
        return cls(cursor.lastrowid, name, location)

    def update_restaurant(self, name=None, location=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if name:
            cursor.execute('UPDATE restaurants SET name = ? WHERE id = ?', (name, self.id))
            self.name = name
        
        if location:
            cursor.execute('UPDATE restaurants SET location = ? WHERE id = ?', (location, self.id))
            self.location = location
        
        conn.commit()
        conn.close()

    def delete_restaurant(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM restaurants WHERE id = ?', (self.id,))
        conn.commit()
        conn.close()
