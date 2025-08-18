# functions go here
def clean_filename(file_name):
    """Check filename has not illegal characters and is not too long"""

    while True:

        # replace spaces with underscores
        file_name = file_name.replace(" ", "_")
        print(f"product name without spaces {file_name}")

        if file_name.isalnum() is True and len(file_name) < 20:
            print("we are ok")
            return file_name
        else:
            print("oops")
            file_name = input("Please enter an alternate name for the start of the file: ")


# loop for testing purposes
while True:
    shop_name = input("Shop Name: ")
    clean_shop_name = clean_filename(shop_name)

    print(f"The original product name was {shop_name}.  The clean version is {clean_shop_name}")