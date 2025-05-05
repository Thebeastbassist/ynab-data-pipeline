import requests
import csv
from datetime import datetime

# Replace this with your Personal Access Token
ACCESS_TOKEN = ''

# Replace this with the name of your budget
TARGET_BUDGET_NAME = 'Budget 2024'

# YNAB API base URL
BASE_URL = 'https://api.ynab.com/v1'

# Set up headers for API requests
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# Get list of budgets
response = requests.get(f'{BASE_URL}/budgets', headers=headers)

# Check if request was successful
if response.status_code != 200:
    print(f"Error fetching budgets: {response.status_code}")
    exit()

budgets_data = response.json()

# Find budget ID for the budget named "Budget 2024"
budget_id = None
for budget in budgets_data['data']['budgets']:
    if budget['name'] == TARGET_BUDGET_NAME:
        budget_id = budget['id']
        break

if not budget_id:
    print(f"Budget '{TARGET_BUDGET_NAME}' not found.")
    exit()

# Get today's date and first day of the year
today = datetime.today().strftime('%Y-%m-%d')
start_of_year = datetime(datetime.today().year, 1, 1).strftime('%Y-%m-%d')

# Get all transactions from this year
transactions_url = f'{BASE_URL}/budgets/{budget_id}/transactions?since_date={start_of_year}'
response = requests.get(transactions_url, headers=headers)

# Check if request was successful
if response.status_code != 200:
    print(f"Error fetching transactions: {response.status_code}")
    exit()

transactions = response.json()['data']['transactions']

# List of payee strings to check for transfer categories
transfer_payees = [
    'Transfer : FREE CHECKING',
    'Transfer : 360 Performance Savings - 360 Performance Savings',
    'Transfer : Capital One'
]

# Convert milliunits to dollars and write to CSV
with open('ynab_transactions_ytd.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Date', 'Account', 'Payee', 'Category', 'Memo', 'Amount'])

    for tx in transactions:
        amount = tx['amount'] / 1000  # Convert from milliunits to dollars

        # Check if payee matches any of the transfer conditions
        if any(transfer_str in tx.get('payee_name', '').lower() for transfer_str in transfer_payees) and category == 'Uncategorized':
            category = 'Transfer'
            print(f"Updated category to 'Transfer' for payee: {tx['payee_name']}")


        # Handle uncategorized transactions and transfer-related payees
        category = tx.get('category_name', 'Uncategorized')  # Default to 'Uncategorized'
        if not category and tx.get('category_id') is None:  # If no category is set
            category = 'Uncategorized'

        # Print debug information to help us understand the issue
        print(f"Transaction: {tx['payee_name']}, Category: {category}")


        # Write the row to the CSV
        writer.writerow([
            tx['date'],
            tx.get('account_name', ''),
            tx.get('payee_name', ''),
            category,
            tx.get('memo', ''),
            amount
        ])

print("✅ YTD transactions saved to ynab_transactions_ytd.csv")
