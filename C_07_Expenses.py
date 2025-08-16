import pandas
from tabulate import tabulate

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


def currency(x):
    """Formats numbers as currency ($#.##)"""
    return "${:.2f}".format(x)


def yes_no(question):
    """Checks that users enter yes / no / y / n"""

    while True:

        response = input(question).lower()

        if response == "y" or response == "yes":
            return "yes"
        elif response == "n" or response == "no":
            return "no"

        print(f"Please answer yes / no (y / n)")
        

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

    # Calculate util column
    util_subtotal = util_frame['Utility Cost'].sum()

    # apply currency formatting
    util_frame['Utility Cost'] = util_frame['Utility Cost'].apply(currency)

    # make into string with desired columns
    utility_string = tabulate(util_frame[['Utility', 'Utility Cost']], headers='keys',
                              tablefmt='psql', showindex=False)

    # make panda
    wage_frame = pandas.DataFrame(wages_dict)

    # Calculate wage Column
    wage_frame['Cost'] = wage_frame['Hours'] * wage_frame['$ / Employee'] * wage_frame['Amount']

    # calculate subtotal
    emp_wage_subtotal = wage_frame['Cost'].sum()

    # Apply currency formatting to currency columns.
    add_dollars = ['$ / Employee', 'Cost']
    for var_item in add_dollars:
        wage_frame[var_item] = wage_frame[var_item].apply(currency)

    # make expense frame into a string with the desired columns

    expense_string = tabulate(wage_frame, headers='keys',
                              tablefmt='psql', showindex=False)

    # return the pandas and subtotals
    return expense_string, emp_wage_subtotal, utility_string, util_subtotal


#loop for testing

# Wage calculations
get_wages = get_expenses("wages")
wage_panda_string = get_wages[0]
wage_subtotal = get_wages[1]

# assumes no utilities
utility_subtotal = 0
utility_panda_string = ""

# asks if user has utilities
print()

# gets utilities if user says yes
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

# calculates total costs
total_cost = wage_subtotal + utility_subtotal

# prints calculations
print(wage_panda_string)
print(utility_panda_string)
print(wage_subtotal)
print(utility_subtotal)
print(total_cost)