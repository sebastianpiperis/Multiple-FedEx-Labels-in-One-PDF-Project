import json
import requests

def read_json_file(file_path):
    """Reads and returns JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def get_token(filename):
    """Reads and returns the access token from a file."""
    with open(filename, 'r') as file:
        return file.read().strip()

def post_data(url, headers, data):
    """Sends a POST request and returns the response including headers and status code."""
    response = requests.post(url, json=data, headers=headers)
    return {
        'headers': dict(response.headers),
        'status_code': response.status_code,
        'text': response.text
    }

def update_token(filename, headers):
    """Updates the access token in the headers."""
    token = get_token(filename)
    headers['Authorization'] = f'Bearer {token}'
    return token

# Constants
URL = "https://webapi1.ielightning.net/api/v1/Reports/Custom/C2RCustomTaskReport/List"
TOKEN_FILE = r'C:\Users\sebas\OneDrive\Documents\LabeltoPDF\TOKEN.TXT'
JSON_DATA_FILE = 'request.json'
MAX_RETRIES = 1

# Main script
data = read_json_file(JSON_DATA_FILE)
token = get_token(TOKEN_FILE)
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
success = False
attempt = 0

while attempt < MAX_RETRIES and not success:
    response_info = post_data(URL, headers, data)

    if response_info['status_code'] == 200:
        response_data = json.loads(response_info['text'])
        order_tracking_mapping = {str(item.get("orderId", "")): None for item in response_data["items"]}
        success = True
        
        print(response_info['text'])  # Debugging
        print("Headers:", response_info['headers'])  # Print headers for debugging
        print("Status Code:", response_info['status_code'])  # Print status code for debugging
        
    else:
        print(response_info['text'])  # Debugging
        print("Headers:", response_info['headers'])  # Print headers for debugging
        print("Status Code:", response_info['status_code'])  # Print status code for debugging
        token = update_token(TOKEN_FILE, headers)
        attempt += 1

# You might want to process order_tracking_mapping or return it
