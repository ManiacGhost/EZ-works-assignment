import requests

base_url = 'http://127.0.0.1:5000'

# Client Signup
signup_payload = {
    'username': 'Harsh101',
    'password': 'HarshPandey',
    'email': 'harshpandey8754@gmail.com'
}

signup_response = requests.post(f'{base_url}/client-user/signup', json=signup_payload)
print(signup_response.json())

# Client Login
login_payload = {
    'username': 'Harsh101',
    'password': 'HarshPandey',
}

login_response = requests.post(f'{base_url}/client-user/login', json=login_payload)
client_token = login_response.json()['token']

# Fetching list of all available files
headers = {
    'Authorization': f'Bearer {client_token}'
}

list_files_response = requests.get(f'{base_url}/client-user/list-files', headers=headers)

# Printing all available files
print('File id\tFile Name\tFile Upload Time')
for file in list_files_response.json()['files']:
    print(f'{file["file_id"]}\t{file["filename"]}\t{file["upload_time"]}')

# Downloading a file
file_id_to_download = input('Please enter the id of the file you wish to download: ')

download_response = requests.get(f'{base_url}/client-user/download-file/{file_id_to_download}', headers=headers)
print(download_response.json())
