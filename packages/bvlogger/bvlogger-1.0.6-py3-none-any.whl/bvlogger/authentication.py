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
        return response.json()
        token = data.get('token')
        project_id = data.get('projectId')
        return token, project_id
