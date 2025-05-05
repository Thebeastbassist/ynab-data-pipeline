import requests

TOKEN = ""
url = "https://api.ynab.com/v1/budgets"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response JSON:")
print(response.json())
