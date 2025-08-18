import pandas


# Functions go here
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
        error = "Oops - please enter a number more than zero."
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
    """Gets utility expenses and outputs
    panda (as a string) and a subtotal of the expenses"""

    # Lists for panda
    all_utility_cost = []
    all_utility = []
    
    utility_dict = {
        "Utility": all_utility,
        "Utility Cost": all_utility_cost
    }

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

    # make panda
    util_frame = pandas.DataFrame(utility_dict)

    # Calculate utility Column
    util_frame['Cost'] = util_frame['Utility Cost']

    # calculate subtotal
    subtotal = util_frame['Cost'].sum()

    # return the expenses panda and the subtotal
    return  util_frame, subtotal


# main routine starts here

print()

print("Getting Utility Costs...")
utility_expenses = get_expenses("utility")
print()
utility_panda = utility_expenses[0]
utility_subtotal = utility_expenses[1]

print(utility_panda)
print(utility_subtotal)
print()
