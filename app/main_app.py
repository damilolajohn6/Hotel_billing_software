import tkinter as tk
from tkinter import Toplevel, Text, BOTH, ttk
from app.menu_manager import MenuManager
from app.order_manager import OrderManager
from app.database_manager import DatabaseManager
from tkinter import messagebox


class RestaurantBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BillEase")
        self.root.geometry("1360x720")  # Set your desired window size
        self.root.iconbitmap("resources/icons/Burger.ico")

        self.menu_manager = MenuManager()
        self.menu_manager.load_menu_from_file("data/menu_data.json")
        self.order_dict = {}
        self.order_manager = OrderManager()
        self.database_manager = DatabaseManager("billing_database.db")

        self.setup_ui()

    def setup_ui(self):
        # Set up UI components and layout
        self.setup_customer_details_frame()
        self.setup_menu_frame()
        self.setup_item_frame()
        self.setup_order_frame()

    def setup_customer_details_frame(self):
        customer_details_frame = ttk.LabelFrame(self.root, text="Customer Details")
        customer_details_frame.pack(side=tk.TOP, padx=10, pady=10)

        # Customer name
        ttk.Label(customer_details_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.customer_name = tk.StringVar()
        ttk.Entry(customer_details_frame, textvariable=self.customer_name).grid(row=0, column=1, padx=10, pady=5)

        # Customer contact
        ttk.Label(customer_details_frame, text="Contact:").grid(row=0, column=2, padx=10, pady=5)
        self.customer_contact = tk.StringVar()
        ttk.Entry(customer_details_frame, textvariable=self.customer_contact).grid(row=0, column=3, padx=10, pady=5)

        # Customer email
        ttk.Label(customer_details_frame, text="Email:").grid(row=1, column=0, padx=10, pady=5)
        self.customer_email = tk.StringVar()
        ttk.Entry(customer_details_frame, textvariable=self.customer_email).grid(row=1, column=1, padx=10, pady=5)

        # Customer address
        ttk.Label(customer_details_frame, text="Address:").grid(row=1, column=2, padx=10, pady=5)
        self.customer_address = tk.StringVar()
        ttk.Entry(customer_details_frame, textvariable=self.customer_address).grid(row=1, column=3, padx=10, pady=5)


    def setup_menu_frame(self):
        menu_frame = ttk.LabelFrame(self.root, text="Menu")
        menu_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Extract category names from menu data
        category_names = [category["category"] for category in self.menu_manager.menu_items]

        # Menu category combobox
        ttk.Label(menu_frame, text="Select Category:").grid(row=0, column=0, padx=10, pady=5)
        self.menu_category_var = tk.StringVar()
        self.menu_category_combobox = ttk.Combobox(menu_frame, textvariable=self.menu_category_var, values=category_names)
        self.menu_category_combobox.grid(row=0, column=1, padx=10, pady=5)

        # Show menu button
        ttk.Button(menu_frame, text="Show Menu", command=self.show_menu).grid(row=0, column=2, padx=20, pady=5)

        # Menu items treeview
        self.menu_treeview = ttk.Treeview(menu_frame, columns=("name", "price"), show="headings")
        self.menu_treeview.heading("name", text="Name")
        self.menu_treeview.heading("price", text="Price")
        self.menu_treeview.grid(row=1, columnspan=3, padx=10, pady=10)

    def show_menu(self):
        # Get the selected category from the combobox
        selected_category = self.menu_category_var.get()

        # Clear existing items in the treeview
        self.menu_treeview.delete(*self.menu_treeview.get_children())

        # Find the selected category in the menu data
        selected_category_data = next((category for category in self.menu_manager.menu_items if category["category"] == selected_category), None)

        if selected_category_data:
            # Populate the treeview with items from the selected category
            for item in selected_category_data["items"]:
                self.menu_treeview.insert("", "end", values=(item["name"], item["price"]))



    def setup_item_frame(self):
        item_frame = ttk.LabelFrame(self.root, text="Item")
        item_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Item name
        ttk.Label(item_frame, text="Name:").grid(row=0, column=0, padx=10, pady=5)
        self.item_name_var = tk.StringVar()
        self.item_name_entry = ttk.Entry(item_frame, textvariable=self.item_name_var, state=tk.DISABLED)
        self.item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        # Item rate
        ttk.Label(item_frame, text="Rate:").grid(row=0, column=2, padx=10, pady=5)
        self.item_rate_var = tk.StringVar()
        self.item_rate_entry = ttk.Entry(item_frame, textvariable=self.item_rate_var, state=tk.DISABLED)
        self.item_rate_entry.grid(row=0, column=3, padx=10, pady=5)

        # Item quantity
        ttk.Label(item_frame, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        self.item_quantity_var = tk.StringVar()
        self.item_quantity_entry = ttk.Entry(item_frame, textvariable=self.item_quantity_var)
        self.item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        # Add to order button
        ttk.Button(item_frame, text="Add to Order", command=self.add_to_order_button_click).grid(row=2, columnspan=4, padx=10, pady=10)


    def add_to_order(self, item):

        name = item["name"]
        rate = item["price"]
        quantity = int(self.item_quantity_var.get())  # Get the quantity from the entry field

        # Add the item to the order_manager
        self.order_manager.add_item_to_order({
            "name": name,
            "rate": float(rate),  # Convert to float
            "quantity": quantity,
            "price": float(rate) * quantity,  # Calculate the price as a float
            "category": item["category"]
        })

        self.update_order_treeview()  # Update the order treeview to reflect the added item


    def remove_from_order(self, category, name):
        item = next((item for item in self.order_manager.get_order_items() if item["name"] == name), None)
        if item:
            self.order_manager.remove_item_from_order(item)


    def clear_order(self):
        self.order_dict = {}

    def add_to_order_button_click(self):
        selected_item = self.get_selected_menu_item()
        if selected_item:
            self.add_to_order(selected_item)  # Pass the selected_item to add_to_order method
            self.update_order_treeview()  # Update the order treeview to reflect the added item


    def get_selected_menu_item(self):
        selected_item = None
        selected_item_id = self.menu_treeview.focus()
        if selected_item_id:
            item_values = self.menu_treeview.item(selected_item_id, "values")
            if item_values:
                selected_item = {
                    "name": item_values[0],  # Name is the first column value
                    "price": item_values[1],  # Price is the second column value
                    "category": self.menu_category_var.get()  # Selected category from combobox
                }
        return selected_item

    # def update_total_price(self):
    #     total_price = sum(item["price"] for item in self.order_manager.get_order_items())
    #     self.total_price_var.set(f"${total_price:.2f}")

    def update_total_price(self):
        total_price = self.order_manager.calculate_total_price()
        self.total_price_var.set(f"${total_price:.2f}")



    def setup_order_frame(self):
        order_frame = ttk.LabelFrame(self.root, text="Your Order")
        order_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Order items treeview
        self.order_treeview = ttk.Treeview(order_frame, columns=("name", "rate", "quantity", "price"), show="headings")
        self.order_treeview.heading("name", text="Name")
        self.order_treeview.heading("rate", text="Rate")
        self.order_treeview.heading("quantity", text="Quantity")
        self.order_treeview.heading("price", text="Price")

        # Set the width of the columns to make the combobox smaller
        self.order_treeview.column("name", width=150)
        self.order_treeview.column("rate", width=80)
        self.order_treeview.column("quantity", width=80)
        self.order_treeview.column("price", width=80)

        self.order_treeview.grid(row=0, columnspan=2, padx=10, pady=10)

        # Total Price
        ttk.Label(order_frame, text="Total Price:").grid(row=1, column=0, padx=10, pady=5)
        self.total_price_var = tk.StringVar()
        self.total_price_label = ttk.Label(order_frame, textvariable=self.total_price_var)
        self.total_price_label.grid(row=1, column=1, padx=10, pady=5)

        # Bill and Cancel buttons
        ttk.Button(order_frame, text="Generate Bill", command=self.generate_bill).grid(row=2, column=0, padx=20, pady=5)
        ttk.Button(order_frame, text="Cancel Order", command=self.cancel_order).grid(row=2, column=1, padx=20, pady=5)

        # Update the order treeview initially
        self.update_order_treeview()


    def generate_bill(self):
        customer_name = self.customer_name.get()
        customer_contact = self.customer_contact.get()
        customer_email = self.customer_email.get()
        customer_address = self.customer_address.get()


        # Check if there are any items in the order
        if not self.order_manager.get_order_items():
            messagebox.showinfo("Error", "Your order list is empty")
            return

        # Check if customer details are provided
        if not customer_name or not customer_contact:
            messagebox.showinfo("Error", "Customer details are required")
            return

        # Validate customer contact
        if not customer_contact.isdigit():
            messagebox.showinfo("Error", "Invalid customer contact")
            return

        # Ask for confirmation to generate the bill
        ans = messagebox.askquestion("Generate Bill", "Are you sure you want to generate the bill?")
        if ans == "no":
            return

        # Create the bill text
        bill_text = self.create_bill_text()

        # Display the bill in a new window
        self.display_bill_window(bill_text)

        # Save the bill to the database
        self.save_bill_to_database(bill_text, customer_name, customer_contact, customer_email, customer_address)

        # Clear order and customer details
        self.order_manager.clear_order()
        self.clear_customer_details()



    def cancel_order(self):
    # Clear the order items and update the order treeview
        self.order_manager.clear_order()
        self.update_order_treeview()



    def update_order_treeview(self):

        self.order_treeview.delete(*self.order_treeview.get_children())  # Clear previous entries
        for item in self.order_manager.get_order_items():

            self.order_treeview.insert("", "end", values=(item["name"], item["rate"], item["quantity"], item["price"]))
        self.update_total_price()



    def create_bill_text(self):
        bill_text = "\t\t\t\tDanna Hotel and Suites\n\t\t\tIfako/ijaiye, Lagos-100215\n"

        bill_text += f"\nCustomer Details:\n"
        bill_text += f"Name: {self.customer_name.get()}\n"
        bill_text += f"Contact: {self.customer_contact.get()}\n"
        bill_text += f"Email: {self.customer_email.get()}\n"
        bill_text += f"Address: {self.customer_address.get()}\n"

        # Add more details to the bill_text
        bill_text += "Order Details:\n"
        for item in self.order_manager.get_order_items():
            bill_text += f"- {item['name']}: {item['quantity']}\n"

        # Calculate total price and add to the bill_text
        total_price = self.order_manager.calculate_total_price()
        bill_text += f"\nTotal Price: ${total_price:.2f}"

        return bill_text



    def display_bill_window(self, bill_text):
        bill_window = Toplevel()
        bill_window.title("Bill")
        bill_window.geometry("670x500+300+100")

        bill_text_area = Text(bill_window, font=("arial", 12))
        bill_text_area.insert(1.0, bill_text)
        bill_text_area.pack(expand=True, fill=BOTH)

        bill_window.protocol("WM_DELETE_WINDOW", lambda: self.on_bill_window_close(bill_window))

    def on_bill_window_close(self, bill_window):
        bill_window.destroy()

    def save_bill_to_database(self, bill_text, customer_name, customer_contact, customer_email, customer_address):
        try:
            self.database_manager.cursor.execute("""
                INSERT INTO Bills (bill_text, customer_name, customer_contact, customer_email, customer_address, date_time)
                VALUES (?, ?, ?, ?, ?, DATETIME('now'))
            """, (bill_text, customer_name, customer_contact, customer_email, customer_address))
            self.database_manager.conn.commit()
            # messagebox.showinfo("Success", "Bill saved to database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bill to database: {str(e)}")




    def clear_customer_details(self):
        self.customer_name.set("")
        self.customer_contact.set("")


    def run(self):
        self.root.mainloop()

