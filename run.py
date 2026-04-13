import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

# Only needed to check the links work.
# Call sales worksheet.
# sales = SHEET.worksheet("sales") 
# Get all the values from the worksheet sales.
# data = sales.get_all_values()
# Print the data to the terminal.
# print(data)

def get_sales_data():
    """
    Get sales figures imput from the user.
    Run a while loop to collect a valid string of data form the user 
    via the terminal, which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data until it is valid.
    """
    while True:

        print("Please enter sales data form the last market.")
        print("Data should be six numbers, separated by a comma")
        print("Example: 10,20,30.40,50,60\n")

        data_str = input("Enter your data here: ")
        print(f"The data provided is {data_str}")
        # Turn the data into a list of numbers.
        sales_data = data_str.split(",")
        # Validate the data.
        if validate_data(sales_data):
            print("Data is validated")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if strings cannot be converted into int
    or if there aren't exactly 6 values.
    """
    try:
        [int(value)for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)} valules")
    except ValueError as e:
        print(f"Invalid data: {e}, please, try again\n")
        return False
    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure substracted form the stock:
    - Positive surplus indicates waste.
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data--- \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[len(stock) - 1]
    # Calculate surplus.
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(worksheet_name, data_row):
    """
    Update the required worksheet. Adds an extra row with the required data.
    """
    print(f"Updating {worksheet_name}...\n")
    worksheet_to_update = SHEET.worksheet(worksheet_name)
    worksheet_to_update.append_row(data_row)
    print(f"{worksheet_name} updated successfully\n")






def main():
    """
    Run all pogram functions.
    """
    data = get_sales_data()
    # Convert data into list of numbers.
    sales_data = [int(num) for num in data]

    update_worksheet("sales", sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet("surplus", new_surplus_data)


print("Welcome to Love Sandwiches Data Automation")

main()
