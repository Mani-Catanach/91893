import math


# rounding function
def round_up(amount, round_val):
    """rounds amount to desired whole number"""
    return int(math.ceil(amount / round_val)) * round_val


# main routine

# loop for testing purposes ask user for test data
while True:
    profit = float(input("Profit Per Pizza: "))
    total_expenses = float(input("Total Expenses: "))
    target = float(input("Profit Goal: "))
    round_to = int(input("Round to: ")) # replace with call to number function integer

    selling_price = (total_expenses * target) / profit
    suggested_price = round_up(selling_price, round_to)

    print(f"Minimum amount is {selling_price:.2f}")
    print(f"Suggested amount is {suggested_price:.2f}")
    print()
