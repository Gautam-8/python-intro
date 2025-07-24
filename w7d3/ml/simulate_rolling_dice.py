import random

sum_equals_7 = 0
sum_equals_2 = 0
sum_greater_than_10 = 0

num_simulations = 10000

for i in range(num_simulations):
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    
    dice_sum = die1 + die2
    
    if dice_sum == 7:
        sum_equals_7 += 1
    if dice_sum == 2:
        sum_equals_2 += 1
    if dice_sum > 10: 
        sum_greater_than_10 += 1

prob_sum_7 = sum_equals_7 / num_simulations
prob_sum_2 = sum_equals_2 / num_simulations
prob_sum_greater_10 = sum_greater_than_10 / num_simulations

print(f"P(Sum = 7): {prob_sum_7:.4f}")
print(f"P(Sum = 2): {prob_sum_2:.4f}")
print(f"P(Sum > 10): {prob_sum_greater_10:.4f}")

print(f"\nActual counts out of {num_simulations} rolls:")
print(f"Sum = 7: {sum_equals_7} times")
print(f"Sum = 2: {sum_equals_2} times")
print(f"Sum > 10: {sum_greater_than_10} times")