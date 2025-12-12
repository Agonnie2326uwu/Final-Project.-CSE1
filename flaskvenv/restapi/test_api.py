import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:5000"

def pretty_print(resp):
    print("Status code:", resp.status_code)
    ct = resp.headers.get("Content-Type", "")
    if "application/json" in ct:
        try:
            print(json.dumps(resp.json(), indent=2))
        except Exception:
            print(resp.text)
    else:
       
        print(resp.text)

def step_login(username="admin", password="password"):
    print("\n=== STEP 1: LOGIN ===")
    url = f"{BASE_URL}/login"
    payload = {"username": username, "password": password}
    resp = requests.post(url, json=payload)
    pretty_print(resp)
    if resp.status_code == 200:
        token = resp.json().get("token")
        print("Token saved.")
        return token
    else:
        print("Login failed. Exiting.")
        sys.exit(1)

def step_create(token, bird_data):
    print("\n=== STEP 2: CREATE BIRD (POST /birds) ===")
    url = f"{BASE_URL}/birds"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    resp = requests.post(url, json=bird_data, headers=headers)
    pretty_print(resp)
    return resp

def step_get_all(format_type="json"):
    print("\n=== STEP 3: GET ALL BIRDS (GET /birds) ===")
    url = f"{BASE_URL}/birds"
    params = {"format": format_type} if format_type else {}
    resp = requests.get(url, params=params)
    pretty_print(resp)
    return resp

def step_get_one(bird_id, format_type="json"):
    print(f"\n=== STEP 4: GET BIRD BY ID (GET /birds/{bird_id}) ===")
    url = f"{BASE_URL}/birds/{bird_id}"
    params = {"format": format_type} if format_type else {}
    resp = requests.get(url, params=params)
    pretty_print(resp)
    return resp

def step_update(token, bird_id, updated_data):
    print(f"\n=== STEP 5: UPDATE BIRD (PUT /birds/{bird_id}) ===")
    url = f"{BASE_URL}/birds/{bird_id}"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    resp = requests.put(url, json=updated_data, headers=headers)
    pretty_print(resp)
    return resp

def step_delete(token, bird_id):
    print(f"\n=== STEP 6: DELETE BIRD (DELETE /birds/{bird_id}) ===")
    url = f"{BASE_URL}/birds/{bird_id}"
    headers = {"Authorization": token}
    resp = requests.delete(url, headers=headers)
    pretty_print(resp)
    return resp

def step_search(name=None, habitat=None, status=None, format_type="json"):
    print("\n=== STEP 7: SEARCH BIRDS (GET /birds/search) ===")
    url = f"{BASE_URL}/birds/search"
    params = {}
    if name:
        params["name"] = name
    if habitat:
        params["habitat"] = habitat
    if status:
        params["status"] = status
    if format_type:
        params["format"] = format_type
    resp = requests.get(url, params=params)
    pretty_print(resp)
    return resp

if __name__ == "__main__":
    print("Make sure your Flask server is running at", BASE_URL)
    print("Starting tests in 2 seconds...")
    time.sleep(2)

    
    token = step_login("admin", "password")

    
    new_bird = {
        "specificname": "Scripted Eagle",
        "scientificname": "Aquila scriptus",
        "habitat": "Hills",
        "status": "Least Concern"
    }
    resp_create = step_create(token, new_bird)

    
    resp_all = step_get_all()
    created_id = None
    if resp_all.status_code == 200:
        try:
            birds = resp_all.json()
            
            for b in birds[::-1]:
                if b.get("specificname") == new_bird["specificname"]:
                    created_id = b.get("idbirds") or b.get("id") or b.get("idbirds")
                    break
            if created_id:
                print("Found created bird id:", created_id)
            else:
                print("Could not auto-detect created bird id. You can change the ID manually in the script.")
        except Exception:
            print("Could not parse JSON from GET /birds to find id.")
    else:
        print("GET /birds failed; can't auto-detect created id.")

    
    if created_id:
        step_get_one(created_id)

        
        updated = {
            "specificname": "Scripted Eagle Updated",
            "scientificname": "Aquila scriptus updated",
            "habitat": "Mountains",
            "status": "Vulnerable"
        }
        step_update(token, created_id, updated)

       
        step_get_one(created_id)

       
        step_delete(token, created_id)

       
        step_get_one(created_id)
    else:
        print("\nSkipping get/update/delete since created id wasn't found automatically.")

    
    step_search(name="Eagle")
    
    step_get_all(format_type="xml")

    print("\nAll done.")
