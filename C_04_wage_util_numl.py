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
    """Gets employee / utility expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_emp = []
    all_utility = []

    # Expenses dictionary
    wages_dict = {
        "Employee": all_emp
    }

    utility_dict = {
        "Utility": all_utility,
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

            all_utility.append(util_name)

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

            all_emp.append(employee_title)

    return all_emp, all_utility


# main routine goes here

print("Getting Variable Costs...")
employee_expenses = get_expenses("wages")
num_type = len(employee_expenses)-1
print(f"You entered {num_type} employee type(s)")

print("Getting fixed Costs...")
utility_expenses = get_expenses("utility")
num_fixed = len(utility_expenses)
print(f"You entered {num_fixed} utilitie(s)")