import requests
import json

# Odoo server details
odoo_url = 'http://localhost:8017'
db = 'sh_17_attendance_log'
# username = 'your_username'
# password = 'your_password'

# URLs
login_url = f'{odoo_url}/web/session/authenticate'
contacts_url = f'{odoo_url}/my_module/get_contacts'

# Step 1: Authenticate and obtain session cookies
login_data = {
    'jsonrpc': '2.0',
    'method': 'call',
    'params': {
        'db': db,
        'login': 'admin',
        'password': 'admin'
    }
}
headers = {'Content-Type': 'application/json'}

# Authenticate user
response = requests.post(login_url, data=json.dumps(login_data), headers=headers)
if response.ok and response.json().get('result'):
    session_cookies = response.cookies
    print("Authenticated successfully.")

    # Step 2: Make a request to get contacts
    response = requests.post(contacts_url,data=json.dumps({}), cookies=session_cookies, headers=headers)

    if response.ok:
        contacts = response.json()
        print("Contacts:", contacts)
    else:
        print("Error fetching contacts:", response.status_code, response.text)
else:
    print("Login failed:", response.status_code, response.text)
