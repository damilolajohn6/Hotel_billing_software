class OrderManager:
    def __init__(self):
        self.order_items = []

    def add_item_to_order(self, item):
        self.order_items.append(item)

    def remove_item_from_order(self, item):
        if item in self.order_items:
            self.order_items.remove(item)

    def update_item_in_order(self, item, quantity):
        for order_item in self.order_items:
            if order_item["name"] == item["name"]:
                order_item["quantity"] = quantity

    def get_order_items(self):
        return self.order_items

    def clear_order(self):
        self.order_items = []

    def calculate_total_price(self):
        total_price = sum(item["price"] for item in self.order_items)
        return total_price
