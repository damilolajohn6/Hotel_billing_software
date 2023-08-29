import json

class MenuManager:
    def __init__(self):
        self.menu_items = []

    def load_menu_from_file(self, file_path):
        with open(file_path, "r") as file:
            self.menu_items = json.load(file)

    def get_menu_items(self):
        return self.menu_items

    def get_menu_items_by_category(self, category):
        items_by_category = []
        for item in self.menu_items:
            if item.get("category") == category:
                items_by_category.append(item)
        return items_by_category
