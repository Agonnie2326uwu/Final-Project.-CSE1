import requests

BASE_URL = "http://127.0.0.1:5000"

def print_result(title, response):
    print(f"\n{title}:")
    print(f"Status: {response.status_code}")
    try:
        print(response.json())
    except:
        print(response.text)

print("LOGIN")
username = input("Username: ")
password = input("Password: ")

login_response = requests.post(f"{BASE_URL}/login", json={
    "username": username,
    "password": password
})
print_result("LOGIN", login_response)

token = login_response.json().get("token")

if not token:
    print("No token received. Exiting.")
    exit()

headers = {
    "Authorization": f"Bearer {token}"
}

print("\nCREATE BIRD")
specificname = input("Specific name: ")
scientificname = input("Scientific name: ")
habitat = input("Habitat: ")
status = input("Status: ")

create_response = requests.post(f"{BASE_URL}/birds", json={
    "specificname": specificname,
    "scientificname": scientificname,
    "habitat": habitat,
    "status": status
}, headers=headers)
print_result("CREATE BIRD", create_response)

all_birds_response = requests.get(f"{BASE_URL}/birds")
birds = all_birds_response.json()
print_result("ALL BIRDS", all_birds_response)

if not birds:
    print("No birds found.")
    exit()

new_id = birds[-1]["idbirds"]
print(f"New Bird ID: {new_id}")

print("\nUPDATE BIRD")
specificname = input("New specific name: ")
scientificname = input("New scientific name: ")
habitat = input("New habitat: ")
status = input("New status: ")

update_response = requests.put(f"{BASE_URL}/birds/{new_id}", json={
    "specificname": specificname,
    "scientificname": scientificname,
    "habitat": habitat,
    "status": status
}, headers=headers)
print_result("UPDATE BIRD", update_response)

delete_confirm = input(f"Delete bird {new_id}? (y/n): ")
if delete_confirm.lower() == "y":
    delete_response = requests.delete(f"{BASE_URL}/birds/{new_id}", headers=headers)
    print_result("DELETE BIRD", delete_response)

final_list = requests.get(f"{BASE_URL}/birds")
print_result("FINAL BIRDS LIST", final_list)
