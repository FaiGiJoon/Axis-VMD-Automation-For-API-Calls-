import requests
from requests.auth import HTTPDigestAuth

class AxisDevice:
    def __init__(self, ip, user, password):
        self.ip = ip
        self.url_base = f"http://{ip}"
        self.session = requests.Session()
        self.session.auth = HTTPDigestAuth(user, password)

    def get(self, path, params=None):
        return self.session.get(f"{self.url_base}{path}", params=params)

    def post(self, path, json_data=None):
        return self.session.post(f"{self.url_base}{path}", json=json_data)
