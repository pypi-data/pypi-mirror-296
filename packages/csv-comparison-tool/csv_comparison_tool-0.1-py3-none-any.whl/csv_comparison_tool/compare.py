# csv_compare_tool/compare.py
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def get_file(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    print(prompt)
    file_path = filedialog.askopenfilename(
        title=prompt,
        filetypes=[("CSV files and Excel files", "*.csv *.xlsx")]
    )
    return file_path

def convert_xlsx_to_csv(file_path, email_col):
    """
    Converts an .xlsx file to a pandas DataFrame and reads only the specified email column.
    """
    try:
        df = pd.read_excel(file_path, usecols=[email_col])
        return df
    except ValueError:
        print(f"Error: Column '{email_col}' not found in {file_path}.")
        return None

def read_backend_csv(backend_file, email_col):
    """
    Reads the backend CSV file, filters to the specified email column, and validates email addresses.
    """
    try:
        backend_df = pd.read_csv(backend_file, index_col=False, header=0, usecols=[email_col])
    except ValueError:
        print(f"Error: Column '{email_col}' not found in {backend_file}.")
        return None
    
    # Regular expression pattern for valid email addresses
    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    # Strip any leading/trailing spaces and filter invalid emails or NaN values
    backend_df[email_col] = backend_df[email_col].str.strip()  # Remove leading/trailing whitespace

    # Apply regex to validate emails and filter the DataFrame
    valid_emails = backend_df[email_col].str.match(email_pattern, na=False)

    # Keep only valid emails
    backend_df = backend_df[valid_emails]

    return backend_df

def compare_email_csvs(customer_df, backend_df, customer_email_col, backend_email_col):
    if customer_df is None or backend_df is None:
        print("Failed to process the files. Make sure the email column names are correct.")
        return

    # Extract the email columns from both files
    customer_emails = customer_df[customer_email_col].dropna().str.lower().unique()
    backend_emails = backend_df[backend_email_col].dropna().str.lower().unique()  # Automatically drops missing values

    # Calculate the number of emails in each file
    num_customer_emails = len(customer_emails)
    num_backend_emails = len(backend_emails)

    # Calculate the difference
    email_difference = num_backend_emails - num_customer_emails

    # Emails in customer file that are not in backend file
    missing_in_backend = set(customer_emails) - set(backend_emails)

    # Output results
    print("\nComparison of Email Addresses Between Files")
    print("="*50)
    print(f"1. Number of email addresses in customer file: {num_customer_emails}")
    print(f"2. Number of email addresses in backend file: {num_backend_emails}")
    print(f"3. Difference (backend - customer): {email_difference}")
    print(f"4. Emails to be deleted (in customer file) but not yet deactivated (not in backend file): ")
    if missing_in_backend:
        for email in missing_in_backend:
            print(f"- {email}")
    else:
        print("None")
    
    return {
        'num_customer_emails': num_customer_emails,
        'num_backend_emails': num_backend_emails,
        'email_difference': email_difference,
        'missing_in_backend': missing_in_backend
    }

def run_local_comparison():
    print("Welcome to the Email CSV Comparison Tool!")

    # Get customer file (can be .csv or .xlsx)
    customer_file = get_file("Select the Customer CSV or Excel (.xlsx) file:")
    backend_file = get_file("Select the Backend CSV file:")

    # Ask for the email column names
    customer_email_col = input("Enter the column name for email addresses in the customer file: ")
    backend_email_col = input("Enter the column name for email addresses in the backend CSV file: ")

    # Check if customer file is .xlsx and convert to DataFrame (read only the email column)
    if customer_file.endswith(".xlsx"):
        customer_df = convert_xlsx_to_csv(customer_file, customer_email_col)
    else:
        customer_df = pd.read_csv(customer_file, usecols=[customer_email_col])

    # Read the backend CSV (read only the email column)
    backend_df = read_backend_csv(backend_file, backend_email_col)

    # Perform comparison
    compare_email_csvs(customer_df, backend_df, customer_email_col, backend_email_col)

def main():
    """Entry point for the tool"""
    run_local_comparison()