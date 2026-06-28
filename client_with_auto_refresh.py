import requests

class SHMRYClient:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base = base_url
        self.access_token = None
        self.refresh_token = None

    def login(self, username, password):
        r = requests.post(f"{self.base}/auth/login", json={"username": username, "password": password})
        data = r.json()
        self.access_token = data["access_token"]
        self.refresh_token = data["refresh_token"]
        return data

    def _request(self, method, endpoint, **kwargs):
        headers = kwargs.pop("headers", {})
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        if self.refresh_token:
            headers["X-Refresh-Token"] = self.refresh_token
        
        r = requests.request(method, f"{self.base}{endpoint}", headers=headers, **kwargs)
        
        if r.status_code == 401 and "expired" in r.text.lower():
            # Auto refresh
            refresh_r = requests.post(f"{self.base}/auth/refresh", json={"refresh_token": self.refresh_token})
            if refresh_r.status_code == 200:
                self.access_token = refresh_r.json()["access_token"]
                return self._request(method, endpoint, **kwargs)  # retry
        return r

    def post_commercial(self, module, data):
        return self._request("POST", f"/commercial/{module}", json=data)

client = SHMRYClient()
print(client.login("badar", "badar123"))
print(client.post_commercial("demand", {"customer": "Badar", "need": "steel"}).json())
