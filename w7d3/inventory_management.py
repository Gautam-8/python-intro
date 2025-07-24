inventory = {
    "apples": {"price": 10, "quantity": 150},
    "bananas": {"price": 5, "quantity": 200},
    "oranges": {"price": 8, "quantity": 120},
}

inventory["grapes"] = {"price": 15, "quantity": 90}
print("Added new product: grapes\n")

inventory["bananas"]["price"] = 6
print("Updated price of bananas to 6\n")

if inventory["apples"]["quantity"] >= 25:
    inventory["apples"]["quantity"] -= 25
    print("Sold 25 apples\n")
else:
    print("Not enough apples in stock to sell\n")

total_value = sum(item["price"] * item["quantity"] for item in inventory.values())
print(f"Total Inventory Value: ₹{total_value}\n")

low_stock = [product for product, info in inventory.items() if info["quantity"] < 100]
print("Low Stock Products (quantity < 100):", low_stock)
