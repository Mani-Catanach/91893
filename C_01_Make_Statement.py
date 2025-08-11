# Functions go here
def make_statement(statement, decoration):
    """Emphasises headings by adding decoration at the start and end"""

    return f"{decoration * 3} {statement} {decoration * 3}"


# Main routine goes here
print(make_statement("Instructions", "[]"))