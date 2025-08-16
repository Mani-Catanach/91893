import pandas
from tabulate import tabulate


#functions go here
def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


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


def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


def pizza_prof_calc():
    # PIZZA list for panda
    all_pizza = []
    all_pizza_cost = []
    all_pizza_sell = []
    all_profit_per_pizza = []

    profit_dict = {
        "Name": all_pizza,
        "Material cost": all_pizza_cost,
        "Sell price": all_pizza_sell,
        "Profit/Pizza": all_profit_per_pizza
    }

    # loop to get expenses
    while True:
        pizza_name = not_blank("Pizza Name: ")

        if pizza_name.lower() == "xxx":
            if len(all_pizza) == 0:
                print("Oops - you have not entered anything.  "
                      "You need at least one item.")
                continue
            else:
                break

        cost_pizza = num_check("$ / Pizza? ", "float")
        mat_cost = num_check("Material Cost?", "float")
        pizza_prof = cost_pizza - mat_cost
        if pizza_prof <= 0:
            print("You cannot have a profit of <=$0 per pizza. Make a new pizza product")
            print()
            continue

        all_pizza.append(pizza_name)
        all_pizza_cost.append(mat_cost)
        all_pizza_sell.append(cost_pizza)
        all_profit_per_pizza.append(pizza_prof)

    # make panda
    pizza_frame = pandas.DataFrame(profit_dict)

    # Calculate Cost Column
    pizza_frame['Profit / Pizza'] = pizza_frame['Sell price'] - pizza_frame['Material cost']

    # calculate subtotal
    pizza_sub = pizza_frame['Profit / Pizza'].sum()
    max_prof = pizza_frame['Profit / Pizza'].max()
    min_prof = pizza_frame['Profit / Pizza'].min()
    avg_prof = pizza_frame['Profit / Pizza'].mean()

    # Apply currency formatting to currency columns.
    add_pizza = ['Sell price', 'Material cost', 'Profit / Pizza']
    for var_item in add_pizza:
        pizza_frame[var_item] = pizza_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    pizza_string = tabulate(pizza_frame[['Name', 'Profit / Pizza']], headers='keys',
                            tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return pizza_string, pizza_sub, avg_prof, max_prof, min_prof


# main routine goes here
print("Getting Pizza Profit")

# get pizza numbers
pizza_panda, pizza_subtotal, average_prof, maximum_prof, minimum_prof = pizza_prof_calc()

# print results
print(pizza_panda)
print(pizza_subtotal)
print(average_prof)
print(maximum_prof)
print(minimum_prof)