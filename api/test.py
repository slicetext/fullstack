import requests

viewer = requests.Session()
response = viewer.post("http://127.0.0.1:5000/api/login", json={"username": "test_user", "password": "test_password"})
print(response)
response = viewer.get("http://127.0.0.1:5000/api/search?q=0")
print(response)
