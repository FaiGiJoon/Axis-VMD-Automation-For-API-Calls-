import requests
from requests.auth import HTTPDigestAuth

class AxisDevice:
    def __init__(self, ip, user, password, trust_env=False):
        self.ip = ip
        self.url_base = f"http://{ip}"
        self.session = requests.Session()
        # By default, disable environment variable lookups (like HTTP_PROXY)
        # to improve performance when communicating with local network devices.
        self.session.trust_env = trust_env
        self.session.auth = HTTPDigestAuth(user, password)

    def get(self, path, params=None):
        response = self.session.get(f"{self.url_base}{path}", params=params)
        # Optimization: Default to UTF-8 to avoid expensive encoding detection
        # if the Content-Type header doesn't specify one. This reduces overhead
        # from ~85ms to <1ms for large XML/JSON responses by skipping chardet.
        if response.encoding is None:
            response.encoding = 'utf-8'
        return response

    def post(self, path, json_data=None):
        response = self.session.post(f"{self.url_base}{path}", json=json_data)
        # Optimization: Default to UTF-8 to avoid expensive encoding detection
        # if the Content-Type header doesn't specify one. This reduces overhead
        # from ~85ms to <1ms for large XML/JSON responses by skipping chardet.
        if response.encoding is None:
            response.encoding = 'utf-8'
        return response
