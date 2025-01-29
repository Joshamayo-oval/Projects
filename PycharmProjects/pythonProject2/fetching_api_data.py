import requests
import pandas as pd
import json
# Credentials
CLIENT_ID = "hs3tdMtTJKKwXK8lnEpWqkqea7mobNActnBYwOypfg4"
CLIENT_SECRET = "mFrybXIr0u25dvVNxcPh_APPQjhM0UoJD1ObY8EbVXk"
SCOPE = "organisations:read squads:read athlete_users:read positions:read athletes_availabilities:read sessions:read athlete_data:read users:read third_party_metrics:read"  # Update scope as needed
#SCOPE = "athlete_users:read athletes_availabilities:read sessions:read athlete_data:read"
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

def fetch_organisation_data(endpoint, token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "User-Agent": "agent",  # Replace 'agent' with your application name
    }
    url = f"{BASE_URL}/organisations"
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()
def process_api(token, endpoint):
    """
    This function takes in the endpoint, fetches, processes the json and outputs a dataframe
    :param endpoint: The endpoint for the API
    :param token: The token for the API
    :return: The dataframe of the processed data
    """

    if endpoint == "organisations":
        api_response = fetch_organisation_data(endpoint, token)
        endpoint_data = api_response.get("data", [])
        # Convert to DataFrame
        if isinstance(endpoint_data, list):
            df = pd.DataFrame(endpoint_data)
            # Save the main data
            filename = f"{endpoint}.csv"
            df.to_csv(filename, index=False)
            print(f"Main data saved successfully: {filename}")
            return df
        else:
            print("Error: 'data' key does not contain a list")
            return None
    else: # For all other endpoints
        api_response = fetch_data(endpoint, token)
        print(f"Fetched {endpoint} data")
        print(type(api_response))
        # print(json.dumps(api_response, indent = 4))

        # Extract the athlete data (list of dictionaries)
        endpoint_data = api_response.get("data", [])

        # Convert to DataFrame
        if isinstance(endpoint_data, list):
            df = pd.DataFrame(endpoint_data)

            # Check if 'athlete_profile_variables' exists and is not empty
            if "athlete_profile_variables" in df.columns:
                nested_data = df.explode("athlete_profile_variables").reset_index(drop=True)  # Explode nested lists into rows

                # Create a separate DataFrame for the nested data
                if not nested_data["athlete_profile_variables"].isnull().all():  # Check if there is any data to normalize
                    nested_df = pd.json_normalize(nested_data["athlete_profile_variables"])
                    nested_df["athlete_id"] = nested_data["id"]  # Add reference to the main data's ID

                    # Save the flattened data
                    nested_filename = f"{endpoint}_athlete_profile_variables.csv"
                    nested_df.to_csv(nested_filename, index=False)
                    print(f"Flattened data saved successfully: {nested_filename}")
                else:
                    print(f"No data to flatten in 'athlete_profile_variables' for endpoint: {endpoint}")
            # Save the main data
            filename = f"{endpoint}.csv"
            df.to_csv(filename, index=False)
            print(f"Main data saved successfully: {filename}")

            return df
        else:
            print("Error: 'data' key does not contain a list")
            return None
# Main function for pulling the data
def main():
    try:
        # Get the access token
        token = get_access_token()
        endpoints = ['athlete_users', 'positions', 'athletes/availabilities', 'sessions','squads','training_variables','staff','third_party_sources','organisations']
        for endpoint in endpoints:
            print(f"Processing endpoint: {endpoint}")
            try:
                # Call process_api for each endpoint
                df = process_api(token, endpoint)
                print(f"Successfully processed and saved data for endpoint: {endpoint}")
            except Exception as e:
                print(f"Error processing endpoint '{endpoint}': {str(e)}")

            print("Processing completed for all endpoints.")
# except Exception as e:
#  print(f"An error occurred in the main function: {str(e)}")
#         athlete_users = fetch_data("athlete_users", token)
#         print("Fetched athlete data")
#         print(type(athlete_users))
#         print(json.dumps(athlete_users, indent=4)
#
#         # Extract the athlete data (list of dictionaries)
#         athlete_data = athlete_users.get("data", [])
#
#         # Convert to DataFrame
#         if isinstance(athlete_data, list):
#             df = pd.DataFrame(athlete_data)
#
#             # Save to CSV
#             df.to_csv("athlete_users1.csv", index=False)
#             print("CSV file saved successfully.")
#         else:
#             print("Error: 'data' key does not contain a list")
#
#       # #  Example: Fetch availability data
#       #   athletes_availabilities = fetch_data("athletes_availabilities", token)
#       #   print("Fetched athletes_availabilities data successfully.")
#       #   athletes_availabilities.to_csv("athletes_availabilities1.csv", index=False)
#       #   print("Saved squads data to athletes_availabilities1.csv.")
#
#         #  Example: Fetch squads data
#         organisations = fetch_data("organisations", token)
#         print("Fetched organisations data successfully.")
#         organisations.to_csv("organisations1.csv", index=False)
#         print("Saved squads data to organisations1.csv.")
#
#         #sessions
#         sessions = fetch_data("sessions", token)
#         print("Fetched sessions data successfully.")
#         sessions.to_csv("sessions.csv", index=False)
#         print("Saved squads data to sessions.csv.")
#
# # sessions
#         third_party = fetch_data("third_party", token)
#         print("Fetched third_party data successfully.")
#         third_party.to_csv("third_party.csv", index=False)
#         print("Saved squads data to third_party.csv.")
# # training data
#         training_data = fetch_data("training_variables", token)
#         print("Fetched training data successfully.")
#         training_data.to_csv("training_variables1.csv", index=False)
#         print("Saved training data to training_variables.csv.")
#
#         # training data
#         positions_data = fetch_data("positions", token)
#         print("Fetched positions data successfully.")
#         positions_data.to_csv("positions.csv", index=False)
#         print("Saved training data to positions.csv.")
#
#         staff_data = fetch_data("staff", token)
#         print("Fetched staff data successfully.")
#         staff_data.to_csv("staff1.csv", index=False)
#         print("Saved staff data to staff.csv.")
#
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
