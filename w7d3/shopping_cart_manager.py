def add_item(cart, item):
    cart.append(item)
    print(f'"{item}" added to the cart.')

def remove_item(cart, item):
    if item in cart:
        cart.remove(item)
        print(f'"{item}" removed from the cart.')
    else:
        print(f'"{item}" is not in the cart.')

def remove_last_item(cart):
    if cart:
        removed = cart.pop()
        print(f'Last item "{removed}" removed from the cart.')
    else:
        print("Cart is already empty.")

def display_sorted(cart):
    if cart:
        print("Items in alphabetical order:")
        for item in sorted(cart):
            print(item)
    else:
        print("Cart is empty.")

def display_cart(cart):
    if cart:
        print("Current cart contents:")
        for idx, item in enumerate(cart):
            print(f"{idx}: {item}")
    else:
        print("Cart is empty.")

cart = []

add_item(cart, "apples")
add_item(cart, "bread")
add_item(cart, "milk")
add_item(cart, "eggs")

remove_item(cart, "bread")

remove_last_item(cart)

display_sorted(cart)

display_cart(cart)
