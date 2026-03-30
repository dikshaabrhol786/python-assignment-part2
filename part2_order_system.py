# ---------------- DATA ----------------
menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"], "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"], "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"], "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4, "items": ["Dal Tadka", "Garlic Naan"], "total": 220.0},
        {"order_id": 5, "items": ["Veg Biryani", "Gulab Jamun"], "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
        {"order_id": 7, "items": ["Butter Chicken", "Veg Biryani"], "total": 570.0},
        {"order_id": 8, "items": ["Garlic Naan", "Gulab Jamun"], "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9, "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"], "total": 270.0},
    ],
}

# ---------------- TASK 1 ----------------

print("\n===== MENU =====")

categories = set(item["category"] for item in menu.values())

for cat in categories:
    print(f"\n===== {cat} =====")
    for name, details in menu.items():
        if details["category"] == cat:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{name:15} ₹{details['price']:6.2f}   [{status}]")

# Basic stats
total_items = len(menu)
available_items = sum(1 for item in menu.values() if item["available"])

most_expensive = max(menu.items(), key=lambda x: x[1]["price"])

cheap_items = [(name, d["price"]) for name, d in menu.items() if d["price"] < 150]

print("\nTotal items:", total_items)
print("Available items:", available_items)
print("Most expensive:", most_expensive[0], most_expensive[1]["price"])

print("\nItems under ₹150:")
for item in cheap_items:
    print(item[0], "-", item[1])


# ---------------- TASK 2 ----------------

cart = []

def add_item(name, qty):
    if name not in menu:
        print(f"{name} not found in menu")
        return

    if not menu[name]["available"]:
        print(f"{name} is unavailable")
        return

    for item in cart:
        if item["item"] == name:
            item["quantity"] += qty
            return

    cart.append({"item": name, "quantity": qty, "price": menu[name]["price"]})


def remove_item(name):
    for item in cart:
        if item["item"] == name:
            cart.remove(item)
            return
    print(f"{name} not in cart")


def show_cart():
    print("\nCurrent Cart:")
    for item in cart:
        print(item)


# Simulation
add_item("Paneer Tikka", 2)
show_cart()

add_item("Gulab Jamun", 1)
show_cart()

add_item("Paneer Tikka", 1)
show_cart()

add_item("Mystery Burger", 1)
add_item("Chicken Wings", 1)

remove_item("Gulab Jamun")
show_cart()

# Order summary
print("\n========== Order Summary ==========")
subtotal = 0

for item in cart:
    total = item["quantity"] * item["price"]
    subtotal += total
    print(f"{item['item']:15} x{item['quantity']}   ₹{total:.2f}")

gst = subtotal * 0.05
final = subtotal + gst

print("----------------------------------")
print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST (5%): ₹{gst:.2f}")
print(f"Total:    ₹{final:.2f}")
print("==================================")


# ---------------- TASK 3 ----------------

import copy

inventory_backup = copy.deepcopy(inventory)

# change one value
inventory["Paneer Tikka"]["stock"] = 5

print("\nChanged Inventory:", inventory["Paneer Tikka"])
print("Backup Inventory:", inventory_backup["Paneer Tikka"])

# restore
inventory = copy.deepcopy(inventory_backup)

# deduct stock
for item in cart:
    name = item["item"]
    qty = item["quantity"]

    if inventory[name]["stock"] < qty:
        print(f"Warning: Only {inventory[name]['stock']} available for {name}")
        inventory[name]["stock"] = 0
    else:
        inventory[name]["stock"] -= qty

# reorder alert
print("\nReorder Alerts:")
for name, data in inventory.items():
    if data["stock"] <= data["reorder_level"]:
        print(f"⚠ {name} low stock: {data['stock']}")

print("\nFinal Inventory:", inventory)
print("Backup Inventory:", inventory_backup)


# ---------------- TASK 4 ----------------

print("\nDaily Revenue:")

daily_revenue = {}

for date, orders in sales_log.items():
    total = sum(order["total"] for order in orders)
    daily_revenue[date] = total
    print(date, ":", total)

best_day = max(daily_revenue, key=daily_revenue.get)
print("Best day:", best_day)

# most ordered item
item_count = {}

for orders in sales_log.values():
    for order in orders:
        for item in order["items"]:
            item_count[item] = item_count.get(item, 0) + 1

most_ordered = max(item_count, key=item_count.get)
print("Most ordered item:", most_ordered)

# add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("\nUpdated Revenue:")

for date, orders in sales_log.items():
    total = sum(order["total"] for order in orders)
    print(date, ":", total)

best_day = max(sales_log, key=lambda d: sum(o["total"] for o in sales_log[d]))
print("New Best day:", best_day)

# enumerate orders
print("\nAll Orders:")
count = 1

for date, orders in sales_log.items():
    for order in orders:
        items = ", ".join(order["items"])
        print(f"{count}. [{date}] Order #{order['order_id']} — ₹{order['total']} — {items}")
        count += 1