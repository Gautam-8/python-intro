item_prices = []
qtys = []
item = None

while item != "done":
    item = input("Enter the price of the item: ")
    if item == "done":
        break
    qty = input("Enter the quantity of the item: ")
    item_prices.append(int(item))
    qtys.append(int(qty))

total = sum(item_prices) * sum(qtys)
tax = total * 0.085

for i in range(len(item_prices)):
    print("item {} : ${}".format(i+1, item_prices[i] * qtys[i]))

print("Total: ${}".format(total))
print("Tax: ${}".format(tax))
print("Grand Total: ${}".format(total + tax))