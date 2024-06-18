# abstraction.py

from encapsulation import FoodOrderingSystem, Restaurant, FoodItem, Order
import sys

def signup(system):
    print("\nSignup")
    username = input("Enter username: ")
    password = input("Enter password: ")
    confirm_password = input("Confirm password: ")
    message = system.register_customer(username, password, confirm_password)
    print(message)

def login(system):
    print("\nLogin")
    username = input("Enter username: ")
    password = input("Enter password: ")
    message = system.login(username, password)
    print(message)
    return message == "Login successful."

def view_locations(system):
    locations = system.view_locations()
    print("Available Locations:")
    for loc in locations:
        print(loc)
    location = input("Enter location: ")
    return location

def view_restaurants(system, location):
    restaurants = system.view_restaurants(location)
    print(f"Restaurants in {location}:")
    for restaurant in restaurants:
        print(restaurant.name)
    restaurant_name = input("Enter restaurant name: ")
    return restaurant_name

def view_menu(system, location, restaurant_name):
    restaurants = system.view_restaurants(location)
    restaurant = next((res for res in restaurants if res.name == restaurant_name), None)
    if restaurant:
        print(f"Menu of {restaurant_name}:")
        for item in restaurant.menu:
            print(f"{item.name}: {item.price}")
    else:
        print("Restaurant not found.")
        return None
    return restaurant

def manage_cart(system, order):
    while True:
        print("\nManage Cart")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. View Cart")
        print("4. Confirm Order")
        print("5. Cancel Order")
        choice = input("Enter your choice: ")

        if choice == '1':
            item_name = input("Enter item name to add: ")
            item = next((item for item in order.restaurant.menu if item.name == item_name), None)
            if item:
                order.add_item(item)
                print(f"{item_name} added to cart.")
            else:
                print(f"{item_name} not found in the menu.")
        elif choice == '2':
            item_name = input("Enter item name to remove: ")
            order.remove_item(item_name)
            print(f"{item_name} removed from cart.")
        elif choice == '3':
            print("Items in Cart:")
            for item in order.food_items:
                print(f"{item.name}: {item.price}")
        elif choice == '4':
            total = order.calculate_total()
            print(f"Order confirmed. Total bill: {total}")
            print("THANK YOU")
            system.orders[order.order_id] = order
            sys.exit()  # Exit the program after confirming the order
        elif choice == '5':
            print("Order canceled.")
            return
        else:
            print("Invalid choice. Please try again.")

def main():
    system = FoodOrderingSystem()

    # Add some sample restaurants and food items
    system.add_restaurant("Warangal", Restaurant("Spicy Hub", [FoodItem("Pizza", 120), FoodItem("Burger", 150)]))
    system.add_restaurant("Hanmakonda", Restaurant("Foodies", [FoodItem("Sandwich", 75), FoodItem("Pasta", 125)]))
    system.add_restaurant("Kazipet", Restaurant("Taste Town", [FoodItem("Tacos", 115), FoodItem("Sushi", 300)]))

    while True:
        print("\nWelcome to the Food Ordering System")
        print("1. Signup")
        print("2. Login")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            signup(system)
        elif choice == '2':
            if login(system):
                location = view_locations(system)
                restaurant_name = view_restaurants(system, location)
                restaurant = view_menu(system, location, restaurant_name)
                if restaurant:
                    order = Order(system.order_id_counter, system.logged_in_customer, restaurant)
                    manage_cart(system, order)
                    system.order_id_counter += 1
                system.logout()
        elif choice == '0':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
