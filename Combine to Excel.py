import os
import json
import pandas as pd

# Function to recursively expand nested categories
def expand_nested_categories(base_info, prefix, data):
    """
    Recursively expands nested categories and adds the information to base_info dictionary.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                expand_nested_categories(base_info, f"{prefix}_{key}", value)
            else:
                base_info[f"{prefix}_{key}"] = value
    else:
        base_info[prefix] = data

# Function to process and transform the data
def process_data(data):
    records = []
    for entry in data:
        base_info = {
            "entity_id": entry.get("id"),
            "entity_name": entry.get("name"),
            "entity_market": entry.get("market"),
            "entity_alias": entry.get("alias"),
            "data_year": entry["season"]["year"] if "season" in entry else None,
            "data_type": entry["season"]["type"] if "season" in entry else None,
        }

        # Expand the 'metrics' category
        metrics = entry.get("record", {})
        if isinstance(metrics, dict):
            for category, stats in metrics.items():
                expand_nested_categories(base_info, f"metrics_{category}", stats)

        # Expand the 'comparative' category
        comparative = entry.get("opponents", {})
        if isinstance(comparative, dict):
            for category, stats in comparative.items():
                expand_nested_categories(base_info, f"comparative_{category}", stats)

        # Add processed records to the list
        records.append(base_info)

    return records

# Function to combine JSON files into an Excel file
def combine_json_to_excel(input_folder, output_file):
    combined_data = []

    if not os.path.exists(input_folder):
        print(f"The directory {input_folder} does not exist.")
        return

    # Iterate through all subfolders and JSON files
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".json"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r') as file:
                        data = json.load(file)

                        if isinstance(data, dict):
                            processed_data = process_data([data])
                            combined_data.extend(processed_data)
                        elif isinstance(data, list):
                            processed_data = process_data(data)
                            combined_data.extend(processed_data)
                except Exception as e:
                    print(f"Error processing file {filename} in {root}: {e}")

    if combined_data:
        df = pd.DataFrame(combined_data)

        try:
            df.to_excel(output_file, index=False, engine='openpyxl')
            print(f"Excel file created successfully: {output_file}")
        except Exception as e:
            print(f"Error saving Excel file: {e}")
    else:
        print("No data was found to combine.")

# Input directory containing JSON files
input_folder = r"c:\Users\YourUsername\Documents\Data"
# Output Excel file path
output_file = r"c:\Users\YourUsername\Documents\combined_data.xlsx"

# Call the function to combine JSON files into an Excel file
combine_json_to_excel(input_folder, output_file)
