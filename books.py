import csv
import requests

api_url = "https://reqres.in/api/users"

response = requests.get(api_url)
if response.status_code == 200:
    data = response.json()
    users = data.get('data', [])
else:
    print(f"failed to fetch data.status_code: {response.status_code}")
    users = []

csv_file = 'users.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['ID', 'Email', 'First Name', 'Last Name', 'Avatar'])

    for user in users:
        user_id = user.get('id', 'N/A')
        email = user.get('email', 'N/A')
        first_name = user.get('first_name', 'N/A')
        last_name = user.get('last_name', 'N/A')
        avatar = user.get('avatar', 'N/A')
        writer.writerow([user_id, email, first_name, last_name, avatar])

print(f"Data has been written to {csv_file}")

