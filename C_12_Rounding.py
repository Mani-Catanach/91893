import math

#f functions go here
def num_check(question, num_type="float", exit_code=None):
    """Checks that response is a float / integer more than zero"""

    if num_type == "float":
        error = "Please enter a number more than 0."
    else:
        error = "Please enter an integer more than 0."

    while True:

        response = input(question)

        # check for exit code and return it if entered
        if response == exit_code:
            return response

        # check datatype is correct and that number
        # is more than zero
        try:

            if num_type == "float":
                response = float(response)
            else:
                response = int(response)

            if response > 0:
                return response
            else:
                print(error)

        except ValueError:
            print(error)


# rounding function
def round_up(amount, round_val):
    """rounds amount to desired whole number"""
    return int(math.ceil(amount / round_val)) * round_val


# main routine

# loop for testing purposes ask user for test data
while True:
    profit = num_check("Profit Per Pizza: ", "float")
    total_expenses = num_check("Total Expenses: ", "float")
    target = num_check("Profit Goal: ", "float")
    round_to = num_check("Round to: ", "integer") # replace with call to number function integer

    selling_price = (total_expenses + target) / profit
    suggested_price = round_up(selling_price, round_to)

    print(f"Minimum amount is {selling_price:.2f}")
    print(f"Suggested amount is {suggested_price:.2f}")
    print()