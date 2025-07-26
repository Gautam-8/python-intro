class Product:
    def __init__(self, name, base_price, discount_percent, stock_quantity, category):
        self.__name = name
        self.__base_price = base_price
        self.__discount_percent = discount_percent
        self.__stock_quantity = stock_quantity
        self.__category = category

        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if not (3 <= len(value) <= 50) or not all(c.isalnum() or c in " -_" for c in value):
            raise ValueError("Name must be 3-50 characters long and can only contain alphanumeric characters, hyphens, and spaces.")
        self.__name = value

    @property
    def base_price(self):   
        return self.__base_price
    @base_price.setter
    def base_price(self, value):
        if value < 0 or value > 50000:
            raise ValueError("Base price must be between $0 and $50,000.")
        self.__base_price = value


    @property
    def discount_percent(self):
        return self.__discount_percent  
    @discount_percent.setter
    def discount_percent(self, value):
        if not (0 <= value <= 75):
            raise ValueError("Discount percent must be between 0% and 75%.")
        self.__discount_percent = round(value, 2)


    @property
    def stock_quantity(self):
        return self.__stock_quantity
    @stock_quantity.setter
    def stock_quantity(self, value):
        if not isinstance(value, int) or value < 0 or value > 10000:
            raise ValueError("Stock quantity must be a non-negative integer and cannot exceed 10,000.")
        self.__stock_quantity = value


    @property
    def category(self):
        return self.__category
    @category.setter
    def category(self, value):
        valid_categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        if value not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}.")
        self.__category = value

    @property
    def final_price(self):
        return round(self.base_price * (1 - self.discount_percent / 100), 2)
    @property
    def savings_amount(self):
        return round(self.base_price * (self.discount_percent / 100), 2)
    @property
    def availability_status(self):
        if self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity < 10:
            return "Low Stock"
        else:
            return "In Stock"
    @property
    def product_summary(self):  
        return f"Product: {self.name}, Base Price: ${self.base_price:.2f}, Discount: {self.discount_percent}%, Final Price: ${self.final_price:.2f}, Stock: {self.availability_status}, Category: {self.category}"
    


# Test Case 1: Valid product creation and automatic calculations
product = Product("Gaming Laptop", 1299.99, 15.5, 25, "Electronics")
assert product.name == "Gaming Laptop"
assert product.base_price == 1299.99
assert product.discount_percent == 15.5
assert abs(product.final_price - 1098.39) < 0.01
assert abs(product.savings_amount - 201.60) < 0.01
assert product.availability_status == "In Stock"

# Test Case 2: Property setters with automatic recalculation
product.discount_percent = 20.567  # Should round to 20.57
assert product.discount_percent == 20.57
assert abs(product.final_price - 1032.24) < 0.01

product.stock_quantity = 5
assert product.availability_status == "Low Stock"

# Test Case 3: Validation edge cases
try:
    product.name = "AB"  # Too short
    assert False, "Should raise ValueError"
except ValueError as e:
    assert "3-50 characters" in str(e)

try:
    product.base_price = -100  # Negative price
    assert False, "Should raise ValueError"
except ValueError:
    pass

try:
    product.category = "InvalidCategory"
    assert False, "Should raise ValueError"
except ValueError:
    pass

# Test Case 4: Product summary formatting
assert "Gaming Laptop" in product.product_summary
assert "1299.99" in product.product_summary
assert "Low Stock" in product.product_summary
