import requests
import pandas as pd

# Credentials
CLIENT_ID = "hs3tdMtTJKwXK8lnEpWqkqea7mobNActnBYwOypfg4"
CLIENT_SECRET = "mFrybXIr0u25dvVNxcPh_APPQjhM0UoJD1ObY8EbVXk"
ORGANIZATION_ID = "199"
BASE_URL = "https://client-api.kitmanlabs.com/api/external/organisations"

# OAuth2 Token Endpoint
TOKEN_URL = f"{BASE_URL}/{ORGANIZATION_ID}/oauth/token"


# Request access token
def get_access_token():
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()["access_token"]


# Fetch data from the endpoint
def fetch_data(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.get(f"{BASE_URL}/{ORGANIZATION_ID}/{endpoint}", headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


# Main logic
def main():
    try:
        # Get the access token
        token = get_access_token()
        print("Access token acquired successfully.")

        # Fetch data from the athlete_users endpoint
        athlete_users_data = fetch_data("athlete_users", token)
        print("Athlete users data fetched successfully.")

        # Fetch data from the squads endpoint
        squads_data = fetch_data("squads", token)
        print("Squads data fetched successfully.")

        # Save athlete_users data to CSV
        df_athletes = pd.DataFrame(athlete_users_data)  # Assuming JSON response is a list of dicts
        df_athletes.to_csv("athlete_users.csv", index=False)
        print("Athlete users data saved to athlete_users.csv.")

        # Save squads data to CSV
        df_squads = pd.DataFrame(squads_data)  # Assuming JSON response is a list of dicts
        df_squads.to_csv("squads.csv", index=False)
        print("Squads data saved to squads.csv.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
