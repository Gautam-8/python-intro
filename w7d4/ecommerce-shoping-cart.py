class Product:
    total_products = 0
    categories = {}

    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        Product.total_products += 1
        if category not in Product.categories:
            Product.categories[category] = 0
        Product.categories[category] += 1

    def get_product_info(self):
        return f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price}, Category: {self.category}, Stock: {self.stock_quantity}"

    @classmethod
    def get_total_products(cls):
        return cls.total_products

    @classmethod
    def get_most_popular_category(cls):
        return max(cls.categories, key=cls.categories.get)
    
class Customer:
    total_revenue = 0

    def __init__(self, customer_id, name, email, membership_type):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership_type = membership_type

    def get_discount_rate(self):
        if self.membership_type == "premium":
            return 20
        elif self.membership_type == "regular":
            return 10
        return 0

    @classmethod
    def get_total_revenue(cls):
        return cls.total_revenue
    
class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, product, quantity):
        if product.stock_quantity < quantity:
            raise ValueError("Not enough stock available")
        self.items.append((product, quantity))
        product.stock_quantity -= quantity

    def remove_item(self, product_id):
        for item in self.items:
            if item[0].product_id == product_id:
                self.items.remove(item)
                item[0].stock_quantity += item[1]
                return True
        return False

    def clear_cart(self):
        for item in self.items:
            item[0].stock_quantity += item[1]
        self.items.clear()

    def get_total_items(self):
        return sum(quantity for _, quantity in self.items)

    def get_subtotal(self):
        return sum(product.price * quantity for product, quantity in self.items)

    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount = (self.customer.get_discount_rate() / 100) * subtotal
        total = subtotal - discount
        Customer.total_revenue += total
        return total

    def place_order(self):
        if not self.items:
            return "Cart is empty"
        return f"Order placed successfully for {self.get_total_items()} items."


# Test Case 1: Creating products with different categories
laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

# Test Case 2: Creating customer and shopping cart
customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

# Test Case 3: Adding items to cart
cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

# Test Case 4: Applying discounts and calculating final price
final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total}")

# Test Case 5: Inventory management
print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

# Test Case 6: Class methods for business analytics
popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: ${total_revenue}")

# Test Case 7: Cart operations
cart.remove_item("P002")  # Remove book
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")

# Expected outputs should show proper product management, cart operations,
# discount calculations, inventory updates, and business analytics
