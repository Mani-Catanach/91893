import pandas
from tabulate import tabulate
from datetime import date
import math


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"


def yes_no(question):
    """Checks that users enter yes / no / y / n"""

    while True:

        response = input(question).lower()

        if response == "y" or response == "yes":
            return "yes"
        elif response == "n" or response == "no":
            return "no"

        print(f"Please answer yes / no (y / n)")


def instructions():
    """Displays instructions"""
    print(make_statement("Instructions", "{}"))

    print('''This program will ask you for... 
    - The name of the product you are selling 
    - How many items you plan on selling 
    - The costs for each component of the product 
      (variable expenses)
    - Whether or not you have utility expenses (if you have 
      utility expenses, it will ask you what they are).
    - How much money you want to make (ie: your profit goal)

It will also ask you how much the recommended sales price should 
be rounded to.

The program outputs an itemised list of the variable and utility 
expenses (which includes the subtotals for these expenses). 

Finally it will tell you how much you should sell each item for 
to reach your profit goal. 

The data will also be written to a text file which has the 
same name as your product and today's date.

    ''')


def not_blank(question):
    """Checks user response is not blank"""
    while True:
        response = input(question)

        if response != "":
            return response
        else:
            print("Sorry, this can't be blank.")


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


def get_expenses(exp_type, how_many=10):
    """Gets variable / utility expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_items = []
    all_amounts = []
    all_employee_cost = []

    # Expenses dictionary
    expenses_dict = {
        "Item": all_items,
        "Amount": all_amounts,
        "$ / Employee": all_employee_cost
    }

    # defaults for utility expenses
    amount = how_many   # how_many defaults to 1
    how_much_question = "Hours per week"

    # loop to get expenses
    while True:

        # Get item name and check it's not blank
        employee_title = not_blank("Employee Title: ")

        # check users enter at least one variable expense
        if exp_type == "wages" and employee_title == "xxx" and len(all_items) == 0:
            print("Oops - you have not entered anything.  "
                  "You need at least one item.")
            continue

        # end loop when users enter exit code
        elif employee_title == "xxx":
            break

        quantity_employee = num_check("Employees of this type: ", "integer")

        # Get variable expenses item amount <enter> defaults to number of
        # products being made.
        if exp_type == "wages":

            amount = num_check(f"Hours per week? <enter for {how_many}>: ",
                               "integer", "")

            # Allow users to push <enter> to default to number of items being made
            if amount == "":
                amount = how_many

            how_much_question = "Wages of title? $"

        # Get price for item (question customised depending on expense type).
        price_for_one = num_check(how_much_question, "float")
        print()

        all_items.append(employee_title)
        all_amounts.append(amount)
        all_employee_cost.append(price_for_one)

    # make panda
    expense_frame = pandas.DataFrame(expenses_dict)

    # Calculate Cost Column
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Employee']

    # calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['Amount', '$ / Employee', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    if exp_type == "variable":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal

# Note: re-enter this later as an argument
# pizza_profit,
def pizza_prof_calc(how_pizza=1):


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
    avg_prof = pizza_frame['Profit / Pizza'].mean

    # Apply currency formatting to currency columns.
    add_pizza = ['Sell price', 'Material cost', 'Profit / Pizza']
    for var_item in add_pizza:
        pizza_frame[var_item] = pizza_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    pizza_string = tabulate(pizza_frame[['Name', 'Profit / Pizza']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return pizza_string, pizza_sub, avg_prof

def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


def profit_goal(total_costs):
    """calculates profit goal work out profit goal and total sales required"""
    # initialise variables and error message
    error = "please enter a valid profit goal\n"
    profit_type = ""
    amount = 0

    valid = False
    while not valid:

        #ask for profit goal...
        response = input("What is your profit goal (eg 500 or 50%)")

        #check if first character is $
        if response[0] == "$":
            profit_type = "$"
            # Get amount everything after the $
            amount = response[:-1]

        elif response[-1] == "%":
            profit_type = "%"
            # get amount ( everything before the %)
            amount = response[:-1]

        else:
            # set response to unknown amount for now
            profit_type = "unknown"
            amount = response

        try:
            # check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = yes_no(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars? , y/n")

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount <= 100:
            percent_type = yes_no(f"Do you mean {amount}%? , y/n: ")
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = "$"

        # return profit goal to main routine
        if profit_type == "$":
            return amount
        else:
            goal = (amount/100) * total_costs
            return goal

def round_up(amount, round_val):
    """Rounds amount to desired hole number"""
    return int(math.ceil(amount / round_val)) * round_val

def clean_filename(raw_filename):
    """Check filename has not illegal characters and is not too long"""

    # assume filename is OK
    valid_filename = True
    error = ""

    while True:

        # replace spaces with underscores
        raw_filename = raw_filename.replace(" ", "_")

        # check for valid length
        if len(raw_filename) >= 20:
            valid_filename = False
            error = ("Oops - your product name / filename is too long.  \n"
                     "Please provide an alternate filename (<= 19 characters) \n"
                     "or press <enter> to default to FRC_yyyy_mm_ddd")

        # iterate through filename and check for invalid characters
        for letter in raw_filename:
            if letter.isalnum() is False and letter != "_":
                valid_filename = False
                error = ("I can't use the product name / proposed filename \n"
                         "as it has illegal characters.  Please \n"
                         "enter an alternate name for the first part \n"
                         "of the file or press <enter> to default to FRC_yyyy_mm_dd")
                break

        if valid_filename is False:
            print(error)
            raw_filename = input("\nPlease enter an alternate name for the start of the file: ")

            # reset valid_filename so that it new name can be checked.
            valid_filename = True

            # put in default filename if users press <enter>
            if raw_filename == "":
                raw_filename = "FRC"

        else:
            return raw_filename


# Main routine goes here

# initialise variables...

# assume we have no utility expenses for now
utility_subtotal = 0
utility_panda_string = ""

print(make_statement("Pizza Cost Calculator", "[]"))

print()
want_instructions = yes_no("Do you want to see the instructions? ")
print()

if want_instructions == "yes":
    instructions()

print()

# Get product details...
product_name = not_blank("Shop Name: ")

# Get variable expenses...
print("Let's get the employee wages....")
employee_wages = get_expenses("wages")
print()

variable_panda_string = employee_wages[0]
employee_subtotal = employee_wages[1]

# ask user if they have utility expenses and retrieve them
print()
has_utility = yes_no("Do you have utility costs? ")

if has_utility == "yes":
    utility_expenses = get_expenses("utility")

    utility_panda_string = utility_expenses[0]
    utility_subtotal = utility_expenses[1]

    # If the user has not entered any utility expenses,
    # # Set empty panda to "" so that it does not display!
    if utility_subtotal == 0:
        has_utility = "no"
        utility_panda_string = ""

total_expenses = employee_subtotal + utility_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

print()
print("Let's get your profit per pizza...")
pi_profit_string, pizza_subtotal, prof_avg = pizza_prof_calc()


# Get profit Goal here.
target = profit_goal(total_expenses)
sales_target = total_expenses + target

# calc min sell price and round it to nearest desired dollar amount
selling_amount = (total_expenses + target) / prof_avg
min_num = math.ceil(selling_amount)
round_to = num_check("Round To: ", 'integer')
suggested_price = round_up(selling_amount, round_to)

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / Strings...
main_heading_string = make_statement(f"Pizza Cost Calculator "
                                     f"({product_name}, {day}/{month}/{year})", "=")
variable_heading_string = make_statement("Employee Wages", "-")
employee_subtotal_string = f"Wage Expense Subtotal: ${employee_subtotal:.2f}"

# set up strings if we have utility costs
if has_utility == "yes":
    utility_heading_string = make_statement("Utility Expenses", "-")
    utility_subtotal_string = f"Utility Expenses Subtotal: {utility_subtotal:.2f}"

# set utility cost strings to blank if we don't have utility costs
else:
    utility_heading_string = make_statement("You have no Utility Expenses", "-")
    utility_subtotal_string = "Utility Expenses Subtotal: $0.00"


selling_amount_heading = make_statement("Selling {price Calculations", "-")
profit_goal_string = f"Profit Goal: ${target:.2f}"
sales_target_string = f"\nTotal Sales Needed: ${sales_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_amount:.2f}"
suggested_price_string = make_statement(f"Suggested Selling Price:"
                                        f"${suggested_price:.2f}", "*")

# List of strings to be outputted / written to file
to_write = [main_heading_string,
            "\n", variable_heading_string, variable_panda_string,
            employee_subtotal_string,
            "\n", utility_heading_string, utility_panda_string,
            utility_subtotal_string, "\n",
            selling_amount_heading, total_expenses_string,
            profit_goal_string, sales_target_string,
            minimum_price_string, "\n", suggested_price_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)

# check product name is suitable for a filename
# and ask for an alternate file name if necessary
clean_product_name = clean_filename(product_name)

file_name = f"{clean_product_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")
