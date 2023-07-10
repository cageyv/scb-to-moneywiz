# This module will contain SCB wrapper functions. It will be used in main.py

import pandas as pd
import logging

def parse_transations(source):
    transaction_data = pd.DataFrame()
    # TODO: Add optional columns input parameter. Try to get these columns from the source, but if not found, use empty values
    parsed_transaction_data = pd.DataFrame(columns=["Date", "Time", "Code/Channel", "Description", "Notes", "Amount"])

    for index, df in enumerate(source):
        # Find the row index containing "Date/Time"
        colum_names_row = df[df.apply(lambda row: row.astype(str).str.contains("Date/Time", case=False).any(), axis=1)].index[0]
        # On the first page we should skip "Balance brought forward" row, which comes under "Date/Time" row
        if index == 0:
            start_row = colum_names_row + 3
        else:
            start_row = colum_names_row + 2
        # Find the row index containing "www.scb.co.th" or "Total Amount"
        end_row = df[df.apply(lambda row: row.astype(str).str.contains("www.scb.co.th|Total Amount", case=False).any(), axis=1)].index[0]

        # Extract the transaction data between the start and end rows
        # And only get first 2 column with data
        transaction_df = df.iloc[start_row:end_row, :2]

        # Append the extracted data to the final dataframe
        transaction_data = pd.concat([transaction_data, transaction_df], ignore_index=True)


    # transaction_data contains 3 row per 1 transaction. 
    # Row 1: [0] Date , [1] DESC : <DESCRIPTION>
    # Row 2: [0] Time, [1] nan ??? 
    # Row 3: [0] Code/Channel (X1 - icome, X2 and other - expense), [1] NOTE : <MY NOTES>

    # Iterate over the rows in the transaction_data DataFrame
    for i in range(0, len(transaction_data), 3):
        date = transaction_data.iloc[i, 0]
        time = transaction_data.iloc[i+1, 0]
        description = transaction_data.iloc[i, 1]
        code_channel = transaction_data.iloc[i+2, 0].split(" ")[0]
        amount = transaction_data.iloc[i+2, 0].split(" ")[1]
        notes = transaction_data.iloc[i+2, 1]

        # Amount formating. Remove comma and convert to float
        amount=float(amount.replace(",", ""))

        # Apply logic for determining the sign of the amount
        if code_channel.startswith('X1'):
            amount *= 1  # positive for X1. X1 - means income
        else:
            amount *= -1  # negative for others. Others - means expense

        # Description formating. Remove DESC :
        description = description.replace("DESC : ", "")

        # Notes formating. Split by spaces and get latest element
        notes = notes.split()[-1]

        # Append the parsed data to the new DataFrame
        parsed_transaction_data = parsed_transaction_data._append({"Date": date, "Time": time, "Description": description, "Code/Channel": code_channel, "Notes": notes, "Amount": amount}, ignore_index=True)

    return parsed_transaction_data

# Function for verify that all transactions are parsed correctly. But using sum of all transactions from source
# Get Total amount and Total Items from source
def get_total(source):

    for df in source:
        # Find the row index containing "Total Amount"
        total_amount_row = df[df.apply(lambda row: row.astype(str).str.contains("Total Amount", case=False).any(), axis=1)].index
        if len(total_amount_row) > 0:
            total_amount = df.iloc[total_amount_row, 0].values.tolist()[0].split(" ")
            total_debit = float(total_amount[-2].replace(",", ""))*(-1)
            total_credit = float(total_amount[-1].replace(",", ""))

        # Find the row index containing "Total Items"
        total_items_row = df[df.apply(lambda row: row.astype(str).str.contains("Total Items", case=False).any(), axis=1)].index
        if len(total_items_row) > 0:
            total_items = df.iloc[total_items_row, 0].values.tolist()[0].split(" ")
            total_items_debit = int(total_items[-2].strip())
            total_items_credit = int(total_items[-1].strip())

    return {"debit":total_debit, "credit":total_credit, "items_debit":total_items_debit, "items_credit":total_items_credit}

# Function for verify that all transactions are parsed correctly. But using sum of all transactions from source
def verify_amounts(parsed_data, total):
    amount_column = "Amount"

    # Filter debit amounts (negative values)
    debit_transactions = parsed_data.loc[parsed_data[amount_column] < 0, amount_column]
    debit_total = debit_transactions.sum()
    debit_total_items = len(debit_transactions)

    # Filter credit amounts (positive values)
    credit_transactions = parsed_data.loc[parsed_data[amount_column] > 0, amount_column]
    credit_total = credit_transactions.sum()
    credit_total_items = len(credit_transactions)

    # Exit with False in case of negative checks 
    
    if debit_total != total["debit"]:
        logging.error("Debit total amount is not equal to the source total amount")
        return False

    if credit_total != total["credit"]:
        logging.error("Credit total amount is not equal to the source total amount")
        return False
    
    if debit_total_items != total["items_debit"]:
        logging.error("Debit total items is not equal to the source total items")
        return False
    
    if credit_total_items != total["items_credit"]:
        logging.error("Credit total items is not equal to the source total items")
        return False
    
    return True
