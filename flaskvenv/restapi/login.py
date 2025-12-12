import requests

BASE_URL = "http://127.0.0.1:5000"

def login():
    url = f"{BASE_URL}/login"
    payload = {
        "username": "admin",
        "password": "password"
    }

    response = requests.post(url, json=payload)
    print("Login Response:", response.json())

    return response.json().get("token")

if __name__ == "__main__":
    token = login()
    print("\nYour token:")
    print(token)
