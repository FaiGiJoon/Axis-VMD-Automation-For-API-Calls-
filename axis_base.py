import requests
from requests.auth import HTTPDigestAuth

class AxisDevice:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.url_base = f"http://{ip}"
        self.auth = HTTPDigestAuth(user, password)

    def get(self, path, params=None):
        return requests.get(f"{self.url_base}{path}", auth=self.auth, params=params)

    def post(self, path, json_data=None):
        return requests.post(f"{self.url_base}{path}", auth=self.auth, json=json_data)