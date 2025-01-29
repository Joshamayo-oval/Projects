# Main function

def process_api(token,endpoint):
    """
    This function takes in the endpoint, fetches, processes the json and outputs a dataframe
    :param endpoint: The endpoint for the API
    :param token: The token for the API
    :return: The dataframe of the processed data
    """
def main():
    try:
        # Get the access token
        token = get_access_token()
        {endpoint}_users = fetch_data(endpoint, token)
        print(f"Fetched {endpoint} data")
        print(type({endpoint}_users))
        print(json.dumps({endpoint}_users, indent=4))

        # Extract the athlete data (list of dictionaries)
        {endpoint}_data = {endpoint}_users.get("data", [])

        # Convert to DataFrame
        if isinstance({endpoint}_data, list):
            df = pd.DataFrame({endpoint}_data)

            # Save to CSV
            df.to_csv("{endpoint}.csv", index=False)
            print("CSV file saved successfully.")
        else:
            print("Error: 'data' key does not contain a list")

    return df