from database.connection import get_db_connection

class Order:
    def __init__(self, id, dish_name, quantity, customer_id, restaurant_id):
        self.id = id
        self.dish_name = dish_name
        self.quantity = quantity
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id

    def __repr__(self):
        return f'<Order {self.dish_name}>'

    def customer(self):
        from models.customer import Customer  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (self.customer_id,))
        customer = cursor.fetchone()
        conn.close()
        
        if customer:
            return Customer(customer['id'], customer['name'], customer['email'])
        return None

    def restaurant(self):
        from models.restaurant import Restaurant  
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM restaurants WHERE id = ?', (self.restaurant_id,))
        restaurant = cursor.fetchone()
        conn.close()
        
        if restaurant:
            return Restaurant(restaurant['id'], restaurant['name'], restaurant['location'])
        return None

    @classmethod
    def create_order(cls, dish_name, quantity, customer_id, restaurant_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (dish_name, quantity, customer_id, restaurant_id)
            VALUES (?, ?, ?, ?)
        ''', (dish_name, quantity, customer_id, restaurant_id))
        conn.commit()
        conn.close()
        
        return cls(cursor.lastrowid, dish_name, quantity, customer_id, restaurant_id)

    def update_order(self, dish_name=None, quantity=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if dish_name:
            cursor.execute('UPDATE orders SET dish_name = ? WHERE id = ?', (dish_name, self.id))
            self.dish_name = dish_name
        
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
