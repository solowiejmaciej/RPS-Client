import requests

for _ in range(1000):
    requests.get("http://127.0.0.1:3000/GetLobbies")