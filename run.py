import gspread
from google.oauth2.service_account import Credentials

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
    Raises ValueError if strings cannot be ocnverted into int
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



data = get_sales_data()
