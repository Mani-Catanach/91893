import pandas


#Functions go here
def not_blank(question):

    while True:
        response = input(question)

        if response != "":
            return response

        print("Sorry, this can't be blank. Please try again. \n")


def num_check(question, num_type="float", exit_code=None):
    """checks user enter integer / float >0"""

    if num_type == "integer":
        error = "Oops - please enter an integer more than zero."
        change_to = int
    else:
        error = "Oops - please enter an integer more than zero."
        change_to = float
    while True:
        response = input(question)

        # check for the xit code
        if response == exit_code:
            return response

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
    """Gets variable / fixed expenses and outputs
    panda as a string and a subtotal of the expenses"""

    # Lists for panda
    all_emp = []
    all_hours = []
    all_amount = []
    all_employee_cost = []

    # Expenses dictionary
    wages_dict = {
        "Employee": all_emp,
        "Hours": all_hours,
        "$ / Employee": all_employee_cost,
        "Amount": all_amount
    }

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

    # make panda
    wage_frame = pandas.DataFrame(wages_dict)

    # Calculate wage Column
    wage_frame['Cost'] = wage_frame['Hours'] * wage_frame['$ / Employee'] * wage_frame['Amount']

    # calculate subtotal
    subtotal = wage_frame['Cost'].sum()

    # return the expenses panda and the subtotal
    return  wage_frame, subtotal


# main routine starts here

print()

print("Getting Variable Costs...")
variable_expenses = get_expenses("wages")
print()
variable_panda = variable_expenses[0]
variable_subtotal = variable_expenses[1]

print(variable_panda)
print(variable_subtotal)
print()