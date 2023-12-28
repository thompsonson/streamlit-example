import requests
from langchain.tools import tool

API_BASE_URL = "https://api.thompson.gr"
TOKEN_URL = "https://api.thompson.gr/token"  # Modify as needed

CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"

def get_access_token():
    """Function to get the OAuth access token."""
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        raise Exception("Failed to obtain access token")

ACCESS_TOKEN = get_access_token()

@tool
def get_groups() -> str:
    """List the groups monitored by the Cyber Threat Intelligence Agent"""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    response = requests.get(f"{API_BASE_URL}/ctia/groups/", headers=headers)
    if response.status_code == 200:
        groups = response.json()
        return f"List of groups: {groups}"
    else:
        return "Error in fetching groups"

@tool
def get_group_description(name: str) -> str:
    """Gets the description for the named group."""
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    params = {"name": name}
    response = requests.get(f"{API_BASE_URL}/ctia/groups/", params=params, headers=headers)
    if response.status_code == 200:
        group_info = response.json()
        return f"Results for query {name}: {group_info}"
    else:
        return f"Error in fetching description for group {name}"

# Example usage
print(get_groups())
print(get_group_description("ExampleGroupName"))
