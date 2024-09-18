import requests

class Auth:
    def __init__(self, base_url):
        self.base_url = base_url

    def login(self, username, password):
        response = requests.post(
            f"{self.base_url}/auth",
            json={
                'username': username,
                'password': password
            }
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()  # Parse the JSON response
        token = data.get('token')
        project_id = data.get('project_Id')
        return token, project_id
