
# https://help.wiz.money/en/articles/4525440-automate-transaction-management-with-url-schemas
# This is moneywiz wrapper module
# It contains all functions for working with MoneyWiz
# It is used in main.py
#

from datetime import datetime
import urllib.parse

# Function for getting MoneyWiz URL for expense or income operations
def get_moneywiz_url(account, amount, currency, date, payee="", description="", memo="", tags="", save=False):

    # Set operation type
    if amount < 0:
        operation = "expense"
        # Make amount positive for MoneyWiz
        amount = abs(amount)
    else:
        operation = "income"

    # Fix account name. It should not contain spaces
    account = account.replace(" ", "")

    # Check amount. It should use dot as decimal delimiter
    if "." not in str(amount):
        raise ValueError("Amount should use dot as decimal delimiter")

    # Currency code should be in uppercase
    currency = currency.upper()

    # Format date as "yyyy-MM-dd HH:mm:ss" for MoneyWiz
    date_obj = datetime.strptime(date, "%d/%m/%y %H:%M")
    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")

    # Create a list to store URL components
    url_components = [
        f"moneywiz://{operation}?account={account}&amount={amount}&currency={currency}&date={formatted_date}"
    ]

    # Add optional parameters
    optional_params = {
        "payee": urllib.parse.quote(payee.strip()),
        "description": urllib.parse.quote(description.strip()),
        "memo": urllib.parse.quote(memo.strip()),
        "tags": urllib.parse.quote(tags.strip()),
    }

    url_components.extend([f"&{key}={value}" for key, value in optional_params.items() if value])

    # Append 'save=true' if save parameter is True
    if save:
        url_components.append("&save=true")

    # Join URL components using str.join()
    moneywiz_url = "".join(url_components).replace(' ', '%20')

    return moneywiz_url
