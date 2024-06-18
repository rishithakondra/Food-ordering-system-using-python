# encapsulation.py

class FoodItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Restaurant:
    def __init__(self, name, menu):
        self.name = name
        self.menu = menu

class Order:
    def __init__(self, order_id, customer, restaurant, food_items=None):
        if food_items is None:
            food_items = []
        self.order_id = order_id
        self.customer = customer
        self.restaurant = restaurant
        self.food_items = food_items

    def add_item(self, food_item):
        self.food_items.append(food_item)

    def remove_item(self, food_item_name):
        self.food_items = [item for item in self.food_items if item.name != food_item_name]

    def calculate_total(self):
        return sum(item.price for item in self.food_items)

class Customer:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class FoodOrderingSystem:
    def __init__(self):
        self.customers = {}
        self.locations = {
            "Warangal": [],
            "Hanmakonda": [],
            "Kazipet": []
        }
        self.orders = {}
        self.order_id_counter = 1
        self.logged_in_customer = None

    def register_customer(self, username, password, confirm_password):
        if username in self.customers:
            return "Username already exists."
        elif password != confirm_password:
            return "Passwords do not match."
        else:
            self.customers[username] = Customer(username, password)
            return "Registration successful."

    def login(self, username, password):
        customer = self.customers.get(username)
        if customer and customer.password == password:
            self.logged_in_customer = customer
            return "Login successful."
        else:
            return "Invalid username or password."

    def logout(self):
        self.logged_in_customer = None
        return "Logged out successfully."

    def add_restaurant(self, location, restaurant):
        if location in self.locations:
            self.locations[location].append(restaurant)
        else:
            print("Invalid location.")

    def view_locations(self):
        return list(self.locations.keys())

    def view_restaurants(self, location):
        if location in self.locations:
            return self.locations[location]
        else:
            return []

    def place_order(self, restaurant_name, food_item_names):
        if not self.logged_in_customer:
            return "Please login to place an order."
        restaurant = None
        for loc in self.locations.values():
            for res in loc:
                if res.name == restaurant_name:
                    restaurant = res
                    break
        if not restaurant:
            return "Restaurant not found."
        
        food_items = []
        for name in food_item_names:
            item = next((item for item in restaurant.menu if item.name == name), None)
            if item:
                food_items.append(item)
            else:
                return f"Food item {name} does not exist in {restaurant_name}."
        
        order = Order(self.order_id_counter, self.logged_in_customer, restaurant, food_items)
        self.orders[self.order_id_counter] = order
        self.order_id_counter += 1
        return f"Order placed successfully. Order ID: {order.order_id}, Total: {order.calculate_total()}"

    def view_orders(self):
        if not self.logged_in_customer:
            return "Please login to view orders."
        return [order for order in self.orders.values() if order.customer == self.logged_in_customer]

    def cancel_order(self, order_id):
        if not self.logged_in_customer:
            return "Please login to cancel orders."
        order = self.orders.get(order_id)
        if order and order.customer == self.logged_in_customer:
            del self.orders[order_id]
            return f"Order ID: {order_id} canceled successfully."
        else:
            return "Order not found or you do not have permission to cancel this order."

    def update_order(self, order_id, add_items=None, remove_items=None):
        if not self.logged_in_customer:
            return "Please login to update orders."
        order = self.orders.get(order_id)
        if not order or order.customer != self.logged_in_customer:
            return "Order not found or you do not have permission to update this order."

        if add_items:
            for item_name in add_items:
                item = next((item for item in order.restaurant.menu if item.name == item_name), None)
                if item:
                    order.add_item(item)
                else:
                    return f"Food item {item_name} does not exist in {order.restaurant.name}."

        if remove_items:
            for item_name in remove_items:
                order.remove_item(item_name)

        return f"Order ID: {order_id} updated successfully."
