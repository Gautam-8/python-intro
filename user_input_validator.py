#user_input_validator 

age = input("Enter your age: ")

try:
    age = int(age)
    if age < 0 or age > 100:
        print("Invalid age")
        age = input("Enter your valid age (0-100): ")
    else:
        print("Valid age")
except ValueError:
    print("Invalid input")
    age = input("Enter your valid age (0-100): ")

else:
    print("Valid age")





