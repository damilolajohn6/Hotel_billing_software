import sqlite3

class DatabaseManager:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_bills_table()

    def save_order_to_database(self, order_items, customer_name, customer_contact):
        try:
            # Insert orders
            for item in order_items:
                self.cursor.execute("""
                    INSERT INTO Orders (name, rate, quantity, price, category)
                    VALUES (?, ?, ?, ?, ?)
                """, (item["name"], item["rate"], item["quantity"], item["price"], item["category"]))

            # Insert customer info
            self.cursor.execute("""
                INSERT INTO CustomerInfo (name, contact)
                VALUES (?, ?)
            """, (customer_name, customer_contact))

            self.conn.commit()  # Commit the changes
        except Exception as e:
            self.conn.rollback()  # Rollback changes if an error occurs
            print(f"Failed to save order to database: {str(e)}")


    def create_bills_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Bills (
                id INTEGER PRIMARY KEY,
                bill_text TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                customer_contact TEXT NOT NULL,
                customer_email TEXT NOT NULL,
                customer_address TEXT NOT NULL,
                date_time DATETIME NOT NULL
            )
        """)
        self.conn.commit()
