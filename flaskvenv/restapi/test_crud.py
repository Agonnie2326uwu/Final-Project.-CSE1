import requests

BASE_URL = "http://127.0.0.1:5000"


TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJleHAiOjE3NjU1NDYzNTN9.8NDGBgzZVMUsx9Byhy_fPbOUSbwVokIDfNifPhU4JU0"

HEADERS = {
    "Authorization": TOKEN
}


def get_all_birds():
    r = requests.get(f"{BASE_URL}/birds")
    print("\nGET /birds:", r.status_code)
    print(r.json())


def create_bird():
    data = {
        "specificname": "Maya.",
        "scientificname": "Lonchura Atricapilla",
        "habitat": "Urban areas",
        "status": "Common"
    }

    r = requests.post(f"{BASE_URL}/birds", json=data, headers=HEADERS)
    print("\nPOST /birds:", r.status_code)
    print(r.json())


def update_bird(id):
    data = {
        "specificname": "Updated Bird",
        "scientificname": "Updated Scientific",
        "habitat": "Forest",
        "status": "Endangered"
    }

    r = requests.put(f"{BASE_URL}/birds/{id}", json=data, headers=HEADERS)
    print("\nPUT /birds/<id>:", r.status_code)
    print(r.json())


def delete_bird(id):
    r = requests.delete(f"{BASE_URL}/birds/{id}", headers=HEADERS)
    print("\nDELETE /birds/<id>:", r.status_code)
    print(r.json())


if __name__ == "__main__":
    print("1. CURRENT BIRDS:")
    get_all_birds()

    print("\n2. ADDING NEW BIRD:")
    create_bird()

    bird_id = int(input("\nEnter ID of bird to update/delete: "))

    print("\n3. UPDATING BIRD:")
    update_bird(bird_id)

    print("\n4. DELETING BIRD:")
    delete_bird(bird_id)

    print("\n5. FINAL BIRDS LIST:")
    get_all_birds()
