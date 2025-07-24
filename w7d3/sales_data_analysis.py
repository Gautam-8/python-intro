sales_data = [
    ("Q1", [("Jan", 1000), ("Feb", 1200), ("Mar", 1100)]),
    ("Q2", [("Apr", 1300), ("May", 1250), ("Jun", 1400)]),
    ("Q3", [("Jul", 1350), ("Aug", 1450), ("Sep", 1300)])
]

print("Total Sales per Quarter:")
for quarter, month_sales in sales_data:
    total = sum(sale for _, sale in month_sales)
    print(f"{quarter}: {total}")

flat_sales = [(month, sale) for _, data in sales_data for (month, sale) in data]
max_month, max_value = max(flat_sales, key=lambda x: x[1])
print(f"\nMonth with Highest Sales: {max_month} ({max_value})")

print("\nFlat List of Monthly Sales:")
print(flat_sales)

print("\nDetailed Monthly Sales with Quarter Info:")
for quarter, months in sales_data:
    for month, value in months:
        print(f"Quarter: {quarter}, Month: {month}, Sales: {value}")
