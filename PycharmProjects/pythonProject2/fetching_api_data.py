import requests
import pandas as pd

# Credentials
CLIENT_ID = "hs3tdMtTJKKwXK8lnEpWqkqea7mobNActnBYwOypfg4"
CLIENT_SECRET = "mFrybXIr0u25dvVNxcPh_APPQjhM0UoJD1ObY8EbVXk"
SCOPE = "organisations:read squads:read athlete_users:read positions:read athlete_data:read users:read"  # Update scope as needed
BASE_URL = "https://client-api.kitmanlabs.com/api/external"
TOKEN_URL = "https://client-api.kitmanlabs.com/oauth/token"
ORGANIZATION_ID = 199

# Function to get access token
def get_access_token():
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "agent",  # Replace 'agent' with your application name
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": SCOPE,
    }
    response = requests.post(TOKEN_URL, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    token = response.json()["access_token"]
    print("Access token acquired successfully.")
    return token


# Function to fetch data from an endpoint
def fetch_data(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "agent",  # Replace 'agent' with your application name
    }
    url = f"{BASE_URL}/organisations/{ORGANIZATION_ID}/{endpoint}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

# Function to fetch data from an endpoint
def fetch_data_athletes(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "agent",  # Replace 'agent' with your application name
    }
    url = f"{BASE_URL}/organisations/{ORGANIZATION_ID}/{endpoint}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
# Main function
def main():
    try:
        # Get the access token
        token = get_access_token()

        # Fetching athletes data
        athlete_data = fetch_data_athletes("athlete_users", token)
        print("Fetched athlete data")

        # Example: Fetch squads data
        # squads_data = fetch_data_users("squads", token)
        # print("Fetched squads data successfully.")

        #
        # squads_df = pd.json_normalize(squads_data)
        # squads_df.to_csv("squads.csv", index=False)
        # print("Saved squads data to squads.csv.")
        #
        # athletes_df = pd.json_normalize(athlete_data)
        # athletes_df.to_csv("athletes.csv", index=False)
        # print("Saved athletes data to athletes.csv.")
        #
        # position_data = fetch_data("positions", token)
        # print("Fetched position data successfully.")
        #
        #
        # positions_df = pd.json_normalize(position_data)
        # positions_df.to_csv("positions.csv", index=False)
        # print("Saved squads data to positions.csv.")

        training_data = fetch_data("training_variables", token)
        print("Fetched training data successfully.")

        training_variables_df = pd.json_normalize(training_data)
        training_variables_df.to_csv("training_variables.csv", index=False)
        print("Saved training data to training_variables.csv.")

        staff_data = fetch_data("staff", token)
        print("Fetched staff data successfully.")

        staff_df = pd.json_normalize(staff_data)
        staff_df.to_csv("staff.csv", index=False)
        print("Saved staff data to staff.csv.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
