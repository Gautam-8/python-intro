products = ["Apples", "Bananas", "Oranges", "Grapes", "Mangoes"]
prices = [30, 10, 25, 40, 50]
quantities = [50, 8, 20, 5, 15]


product_price_pairs = list(zip(products, prices))
print("Product-Price Pairs:", product_price_pairs)


catalog = {
    product: {"price": price, "quantity": quantity}
    for product, price, quantity in zip(products, prices, quantities)
}
print("Product Catalog:")
for product, info in catalog.items():
    print(f"{product}: ₹{info['price']} (Qty: {info['quantity']})")


print("Low Stock Products:")
for product, info in catalog.items():
    if info["quantity"] < 10:
        print(product)
