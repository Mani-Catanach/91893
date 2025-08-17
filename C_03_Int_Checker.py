# Functions go here
def int_check(question):
    """ Checks users enter an integer"""

    error = "Oops - please enter an integer"

    while True:

        try:
            # return the response if it's an integer
            response = int(input(question))

            return response

        except ValueError:
            print(error)


# loop for testing purposes

# asks user how many hours their employee is working for
hours = int_check("Hours per week: ")
print(f"Your employee is working {hours} hours per week")