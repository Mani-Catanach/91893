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
    - The name of the pizza shop you have 
    - The title of your employees
    - The amount of each employee type (must be greater than 0)
    - The amount of hours each employee type works (must be greater than 0) 
    - The wages of that employee type (must be greater than $23.50)
    - Whether or not you have utility expenses (if you have 
      utility expenses, it will ask you what they are).
    - The name of your pizza
    - How much you sell each pizza for
    - How much it costs to make each pizza (must be less than the sell price)
    - Type 'xxx' into the name input when you're done with a section to move on to the next section.
    - You must have at least one entry for each section before moving on to the next 


The program outputs an itemised list of the employee and utility 
expenses (which includes the subtotals for these expenses). It also
outputs the profit you make per pizza and how many pizzas you need to 
sell on average, minimum, and maximum, to break even (rounded up).

The data will then be written to a text file which has the 
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
    all_emp = []
    all_hours = []
    all_amount = []
    all_employee_cost = []
    all_utility_cost = []
    all_utility = []

    # Expenses dictionary
    wages_dict = {
        "Employee": all_emp,
        "Hours": all_hours,
        "$ / Employee": all_employee_cost,
        "Amount": all_amount
    }

    utility_dict = {
        "Utility": all_utility,
        "Utility Cost": all_utility_cost
    }

    if exp_type == "utility":
        # loop to get utilities
        while True:
            util_name = not_blank("Utility Name: ")

            # check users enter at least one utility expense
            if util_name == "xxx" and len(all_utility) == 0:
                print("Oops - you have not entered any utilities.  "
                      "You need at least one item.")
                continue

            # end loop when users enter exit code
            elif util_name == "xxx":
                break

            util_cost = num_check("Utility Cost: ", "float")

            all_utility.append(util_name)
            all_utility_cost.append(util_cost)

    elif exp_type == "wages":
        # loop to get wages
        while True:

            # Get item name and check it's not blank
            employee_title = not_blank("Employee Title: ")

            # check users enter at least one employee
            if employee_title == "xxx" and len(all_emp) == 0:
                print("Oops - you have not entered anything.  "
                      "You need at least one item.")
                continue

            # end loop when users enter exit code
            elif employee_title == "xxx":
                break

            quantity_employee = num_check("Employees of this type: ", "integer")

            hours = num_check(f"Hours per week? <enter for {how_many}>: ",
                              "integer", "")

            # Allow users to push <enter> to default to number of items being made
            if hours == "":
                hours = how_many

            how_much_question = "Wages of title? $"

            # Get price for item (question customised depending on expense type).
            employee_wage = num_check(how_much_question, "float")
            print()

            # loop restarts for illegal/unethical inputs
            if employee_wage < 23.50:
                print("You cannot pay employees less than minimum wage ($23.50). Make a new employee type")
                print()
                continue

            elif hours > 70:
                print("You cannot have an employee work over 70 hours a week. Make a new employee type")
                print()
                continue

            all_emp.append(employee_title)
            all_amount.append(quantity_employee)
            all_hours.append(hours)
            all_employee_cost.append(employee_wage)

    # make util panda
    util_frame = pandas.DataFrame(utility_dict)
    util_subtotal = util_frame['Utility Cost'].sum()
    util_frame['Utility Cost'] = util_frame['Utility Cost'].apply(currency)
    utility_string = tabulate(util_frame[['Utility', 'Utility Cost']], headers='keys',
                              tablefmt='psql', showindex=False)

    # make panda
    wage_frame = pandas.DataFrame(wages_dict)

    # Calculate wage Column
    wage_frame['Cost'] = wage_frame['Hours'] * wage_frame['$ / Employee'] * wage_frame['Amount']

    # calculate subtotal
    subtotal = wage_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['$ / Employee', 'Cost']
    for var_item in add_dollars:
        wage_frame[var_item] = wage_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns

    expense_string = tabulate(wage_frame, headers='keys',
                              tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal, utility_string, util_subtotal


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


def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


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
                     "or press <enter> to default to PCC_yyyy_mm_ddd")

        # iterate through filename and check for invalid characters
        for letter in raw_filename:
            if letter.isalnum() is False and letter != "_":
                valid_filename = False
                error = ("I can't use the product name / proposed filename \n"
                         "as it has illegal characters.  Please \n"
                         "enter an alternate name for the first part \n"
                         "of the file or press <enter> to default to PCC_yyyy_mm_dd")
                break

        if valid_filename is False:
            print(error)
            raw_filename = input("\nPlease enter an alternate name for the start of the file: ")

            # reset valid_filename so that it's new name can be checked.
            valid_filename = True

            # put in default filename if users press <enter>
            if raw_filename == "":
                raw_filename = "PCC"

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
shop_name = not_blank("Shop Name: ")

# Get variable expenses...
print("Let's get the employee wages....")
employee_wages = get_expenses("wages")
print()

employee_panda_string = employee_wages[0]
employee_subtotal = employee_wages[1]

# ask user if they have utility expenses and retrieve them
print()
has_utility = yes_no("Do you have utility costs? ")

if has_utility == "yes":
    utility_expenses = get_expenses("utility")

    utility_panda_string = utility_expenses[2]
    utility_subtotal = utility_expenses[3]

    # If the user has not entered any utility expenses,
    # # Set empty panda to "" so that it does not display!
    if utility_subtotal == 0:
        has_utility = "no"
        utility_panda_string = ""

total_expenses = employee_subtotal + utility_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"

print()
print("Let's get your profit per pizza...")
pi_profit_string, pizza_subtotal, prof_avg, prof_max, prof_min = pizza_prof_calc()
pizza_panda_string = pi_profit_string

# calc amounts to sell
avg_amount = total_expenses / prof_avg
min_amount = total_expenses / prof_max
max_amount = total_expenses / prof_min
avg_num = math.ceil(avg_amount)
min_num = math.ceil(min_amount)
max_num = math.ceil(max_amount)

min_amount = []
max_amount = []
ave_amount = []

# Final dictionary
final_dict = {
    "Minimum Amount": min_amount,
    "Maximum Amount": max_amount,
    "Average Amount": ave_amount
}


min_amount.append(min_num)
max_amount.append(max_num)
ave_amount.append(avg_num)

# make panda
final_frame = pandas.DataFrame(final_dict)
final_panda_string = tabulate(final_frame, headers='keys',
                            tablefmt='psql', showindex=False)

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / Strings...
main_heading_string = make_statement(f"Pizza Cost Calculator "
                                     f"({shop_name}, {day}/{month}/{year})", "=")

employee_heading_string = make_statement("Employee Wages", "-")
employee_subtotal_string = f"Wage Expense Subtotal: ${employee_subtotal:.2f}"

# set up strings if we have utility costs
if has_utility == "yes":
    utility_heading_string = make_statement("Utility Expenses", "-")
    utility_subtotal_string = f"Utility Expenses Subtotal: {utility_subtotal:.2f}"

# set utility cost strings to blank if we don't have utility costs
else:
    utility_heading_string = make_statement("You have no Utility Expenses", "-")
    utility_subtotal_string = "Utility Expenses Subtotal: $0.00"

pizza_profit_heading = make_statement("Profit Per Pizza", "-")
avg_amount_heading = make_statement("Selling Amount Calculations", "-")

print(final_frame)
suggest_amount_string = make_statement(f"We suggest you should sell {avg_num} pizzas per week to break even.", "*")

# List of strings to be outputted / written to file
to_write = [
            main_heading_string,
            "\n", employee_heading_string, employee_panda_string,
            employee_subtotal_string,
            "\n", utility_heading_string, utility_panda_string,
            utility_subtotal_string, "\n",
            pizza_panda_string, "\n",
            total_expenses_string,
            avg_amount_heading, final_panda_string,
            "\n", suggest_amount_string]

# Print area
print()
for item in to_write:
    print(item)

# create file to hold data (add .txt extension)

# check product name is suitable for a filename
# and ask for an alternate file name if necessary
clean_shop_name = clean_filename(shop_name)

file_name = f"{clean_shop_name}_{year}_{month}_{day}"
write_to = "{}.txt".format(file_name)

text_file = open(write_to, "w+")

# write item to file
for item in to_write:
    text_file.write(item)
    text_file.write("\n")