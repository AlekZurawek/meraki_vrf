import csv
import requests

# Meraki API key and organization ID
API_KEY = "enter your API Key here"
ORG_ID = "enter your org ID here"

# Base URL for Meraki API
BASE_URL = "https://api.meraki.com/api/v1"

# Function to create a policy object group
def create_policy_object_group(name):
    endpoint = f"/organizations/{ORG_ID}/policyObjects/groups"
    url = BASE_URL + endpoint
    headers = {
        "X-Cisco-Meraki-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "category": "NetworkObjectGroup",
        "name": name,
        "objectIds": []
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["id"]

# Function to check if a policy object group exists and return its ID
def get_policy_object_group_id(name):
    endpoint = f"/organizations/{ORG_ID}/policyObjects/groups"
    url = BASE_URL + endpoint
    headers = {
        "X-Cisco-Meraki-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    for group in response.json():
        if group["name"] == name:
            return group["id"]
    return None

# Read data from CSV file and process
with open("data.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row["name"]
        cidr = row["CIDR"]
        group_ids = row["groupIds"]

        # Check if policy object group exists or create one
        group_id = get_policy_object_group_id(group_ids)
        if group_id is None:
            group_id = create_policy_object_group(group_ids)

        # Create policy object
        endpoint = f"/organizations/{ORG_ID}/policyObjects"
        url = BASE_URL + endpoint
        headers = {
            "X-Cisco-Meraki-API-Key": API_KEY,
            "Content-Type": "application/json"
        }
        data = {
            "category": "network",
            "cidr": cidr,
            "name": name,
            "type": "cidr",
            "groupIds": [group_id]
        }
        response = requests.post(url, headers=headers, json=data)
        print(f"Policy object created for '{name}' with ID: {response.json()['id']}")
