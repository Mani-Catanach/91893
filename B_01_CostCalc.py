import pandas
from tabulate import tabulate
from datetime import date
import math


# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration
    at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}\n"


def string_check(question, valid_answers, numletters=1):
    """Checks that users enter the full word
    or the 'n' letter/s of a word from a range of valid responses"""

    while True:

        response = input(question).lower()

        for item in valid_answers:

            # check if the response is the entire word
            if response == item:
                return item
            elif response == item[:numletters]:
                return item
        print(f"Please choose an option from {valid_answers}")

def instructions():
    """Displays instructions"""
    print(make_statement("Instructions", "{}"))

    print('''This program will ask you for... 
    - The name of the product you are selling 
    - How many items you plan on selling 
    - The costs for each component of the product 
      (variable expenses)
    - Whether or not you have fixed expenses (if you have 
      fixed expenses, it will ask you what they are).
    - How much money you want to make (ie: your profit goal)

It will also ask you how much the recommended sales price should 
be rounded to.

The program outputs an itemised list of the variable and fixed 
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


def cost(expense_profit, how_many=1):
    """Gets variable / fixed expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_week = []
    all_items = []
    all_dollar_per_pizza = []
    all_sell_pizza = []
    all_employee = []
    all_cost = []

    # Expenses dictionary
    costs_dict = {
        "Cost / Week"
        "Cost Total": all_cost
    }

    profit_dict = {
        "Pizza Name": all_items,
        "Pizza Sell $": all_sell_pizza,
        "Cost To Make?": all_dollar_per_pizza
    }

    # defaults for fixed expenses
    amount = how_many   # how_many defaults to 1
    how_much_question = "How much? $"

    # loop to get profit/expenses
    while True:

        # Get item name and check it's not blank

        wage_question = "Employee wages? $"
        hours_question = "Hours / week?"

        expense_profit = string_check("Costs or profits?", ("cost", "profit"), 1)
        if expense_profit == "cost":
            emp_util = string_check("Utilities or wages?", ("utilities", "wages"), 1)

            # check users enter at least one variable expense
            if emp_util == "xxx" and len(all_items) == 0:
                print("Oops - you have not entered anything.  "
                      "You need at least .")
                continue

            # end loop when users enter exit code
            elif emp_util== "xxx":
                break

            # Get variable expenses item amount <enter> defaults to number of
            # products being made.
            if emp_util == "wage":
                employee_title = not_blank("Employee Title: ")
                amount = num_check(f"How many employees? <enter for {how_many}>: ",
                                   "integer", "")

                # Allow users to push <enter> to default to number of items being made
                if amount == "":
                    amount = how_many

            elif emp_util == "utilities":
                one_or_continuous = string_check("Is this a one off or is it a weekly cost?",
                                                 ("one off", "weekly"))
                utility_name = not_blank("Utility Name: ")
                if one_or_continuous == "weekly":
                    util_cost = num_check("Cost per week: ", "float")

                elif one_or_continuous == "one off":
                    one_off = num_check("Purchase Price: ", "float")

            # Get price for item (question customised depending on expense type).
            wage = num_check(wage_question, "float")
            print()
            hours = num_check(hours_question, "integer")
            week_amount = num_check("How many weeks are you do you want cost calculated for: ", "integer")
            cost_week = hours * wage * amount + util_cost + one_off / week_amount
            cost_total = cost_week * week_amount
            print(cost_week)
            all_week.append(cost_week)
            all_cost.append(cost_total)

        elif expense_profit == "profit":
            pizza_name = not_blank("Pizza Name: ")
            cost_pizza = num_check("$ / Pizza? ", "float")
            mat_cost = num_check("Food Cost?", "float")
            pizza_prof = cost_pizza - mat_cost

            all_dollar_per_pizza.append(cost_pizza)
            all_sell_pizza.append(pizza_prof)

    # make panda
    expense_frame = pandas.DataFrame(costs_dict)

    # Calculate Cost Column
    expense_frame['Cost'] = expense_frame['Amount'] * expense_frame['$ / Item']

    # calculate subtotal
    subtotal = expense_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['Amount', '$ / Item', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns
    if expense_profit == "cost":
        expense_string = tabulate(expense_frame, headers='keys',
                                  tablefmt='psql', showindex=False)
    else:
        expense_string = tabulate(expense_frame[['Item', 'Cost']], headers='keys',
                                  tablefmt='psql', showindex=False)

    # return the expenses panda and subtotal
    return expense_string, subtotal


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
            dollar_type = string_check(f"Do you mean ${amount:.2f}. ie {amount:.2f} dollars? , y/n")

            # set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = "$"
            else:
                profit_type = "%"

        elif profit_type == "unknown" and amount <= 100:
            percent_type = string_check(f"Do you mean {amount}%? , y/n: ")
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

            # reset valid_filename so that new name can be checked.
            valid_filename = True

            # put in default filename if users press <enter>
            if raw_filename == "":
                raw_filename = "FRC"

        else:
            return raw_filename


# Main routine goes here

# intialise variables...

# assume we have no fixed expenses for now
fixed_subtotal = 0
fixed_panda_string = ""

print(make_statement("Pizza Cost Calculator", "[]"))

print()
want_instructions = string_check("Do you want to see the instructions? ", ("yes", "no"), numletters=1).lower()
print()

if want_instructions == "yes":
    instructions()

print()
# Get product details...
product_name = not_blank("Product Name: ")
quantity_made = num_check("Quantity being made: ", "integer")

# Get variable expenses...
print("Let's get the variable expenses....")
variable_expenses = cost("variable", quantity_made)

variable_panda_string = variable_expenses[0]
variable_subtotal = variable_expenses[1]

# ask user if they have fixed expenses and retrieve them
print()
has_fixed = string_check("Do you have fixed expenses? ", ("yes",  "no"), 1)

if has_fixed == "yes":
    fixed_expenses = cost("fixed")

    fixed_panda_string = fixed_expenses[0]
    fixed_subtotal = fixed_expenses[1]

    # If the user has not entered any fixed expenses,
    # # Set empty panda to "" so that it does not display!
    if fixed_subtotal == 0:
        has_fixed = "no"
        fixed_panda_string = ""

total_expenses = variable_subtotal + fixed_subtotal
total_expenses_string = f"Total Expenses: ${total_expenses:.2f}"


# Get profit Goal here.
target = profit_goal(total_expenses)
sales_target = total_expenses + target

# calc min sell price and round it to nearest desired dollar amount
selling_price = (total_expenses +target) / quantity_made
round_to = num_check("Round To: ", 'integer')
suggested_price = round_up(selling_price, round_to)

# strings / output area

# **** Get current date for heading and filename ****
today = date.today()

# Get day, month and year as individual strings
day = today.strftime("%d")
month = today.strftime("%m")
year = today.strftime("%Y")

# Headings / Strings...
main_heading_string = make_statement(f"Pizza Cost Calculator"
                                     f"({product_name}, {day}/{month}/{year})", "=")
quantity_string = f"Quantity being made: {quantity_made}"
variable_heading_string = make_statement("Variable Expenses", "-")
variable_subtotal_string = f"Variable Expenses Subtotal: ${variable_subtotal:.2f}"

# set up strings if we have fixed costs
if has_fixed == "yes":
    fixed_heading_string = make_statement("Fixed Expenses", "-")
    fixed_subtotal_string = f"Fixed Expenses Subtotal: {fixed_subtotal:.2f}"

# set fixed cost strings to blank if we don't have fixed costs
else:
    fixed_heading_string = make_statement("You have no Fixed Expenses", "-")
    fixed_subtotal_string = "Fixed Expenses Subtotal: $0.00"


selling_price_heading = make_statement("Selling {rice Calculations", "-")
profit_goal_string = f"Profit Goal: ${target:.2f}"
sales_target_string = f"\nTotal Sales Needed: ${sales_target:.2f}"

minimum_price_string = f"Minimum Selling Price: ${selling_price:.2f}"
suggested_price_string = make_statement(f"Suggested Selling Price:"
                                        f"${suggested_price:.2f}", "*")

# List of strings to be outputted / written to file
to_write = [main_heading_string, quantity_string,
            "\n", variable_heading_string, variable_panda_string,
            variable_subtotal_string,
            "\n", fixed_heading_string, fixed_panda_string,
            fixed_subtotal_string, "\n",
            selling_price_heading, total_expenses_string,
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