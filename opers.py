import requests

base_url = 'http://127.0.0.1:5000'

login_credentials = {
    'username': 'john_doe',
    'password': 'secure_password'
}

login_response = requests.post(f'{base_url}/ops-user/login', headers=login_credentials)
print(login_response.json())

ops_user_authentication_token = login_response.json()['token']
print(ops_user_authentication_token)

file_name_to_upload = 'test2.xlsx'
file_path_to_upload = f'./{file_name_to_upload}'

file_to_upload = {'file': (f'{file_name_to_upload}', open(file_path_to_upload, 'rb'))}

headers_for_upload = {'Authorization': ops_user_authentication_token}

upload_response = requests.post(f'{base_url}/ops-user/upload-file', files=file_to_upload, headers=headers_for_upload)
print(upload_response.json())
