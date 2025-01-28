import pandas as pd
import json

NAME = 'Joshu'
df = pd.read_csv('C:\\Users\\josha\\PycharmProjects\\pythonProject2\\organisations.csv')

# Fix the JSON format
if 'data' in df.columns:  # Replace 'data' with the actual column containing JSON if necessary
    # Preprocess the data column to ensure valid JSON
    def fix_json_format(json_str):
        try:
            # Replace single quotes with double quotes and parse JSON
            return json.loads(json_str.replace("'", '"'))
        except json.JSONDecodeError:
            return None  # Return None for invalid JSON

    # Apply the fix and parse JSON
    df['parsed_data'] = df['data'].apply(fix_json_format)

    # Drop rows with invalid JSON
    df = df.dropna(subset=['parsed_data'])

    # Expand the JSON into a DataFrame
    df_cleaned = pd.DataFrame(df['parsed_data'].tolist())

    # Display the cleaned DataFrame
    print(df_cleaned.head())
else:
    print("The column containing JSON data was not found.")
print(df.head())


