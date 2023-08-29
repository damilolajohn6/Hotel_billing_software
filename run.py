import tkinter as tk
from app.main_app import RestaurantBillingApp

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantBillingApp(root)
    app.run()
