import csv
import json

def csv_to_json(csv_file_path, json_file_path):
    # Read CSV file and convert it to a list of dictionaries
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = list(csv_reader)

    # Write the list of dictionaries to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Replace 'input.csv' and 'output.json' with your file paths
csv_to_json('filtered_feature.csv', 'filtered_feature.json')