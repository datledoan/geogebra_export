import pandas as pd
import json
import re
import os
import argparse
import yaml

# Function to convert HTML table to JSON
def html_table_to_json(html_filename, json_filename):
    # Read HTML file into a list of DataFrames
    tables = pd.read_html(html_filename)

    if not tables:
        print("No tables found in the HTML file.")
        return

    # Assuming the first table is the target table
    target_table = tables[0]

    # Save the table to a JSON file
    target_table.to_json(json_filename, orient='records', lines=False,index=True)

    with open(json_filename, 'r') as json_file:
        json_data = json.load(json_file)
    for i, item in enumerate(json_data):
        item['id'] = i + 1
    with open(json_filename, 'w') as output_file:
        json.dump(json_data, output_file, indent=2)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Convert HTML table to graph in JSON')
    parser.add_argument('--html_file', type=str, default='test_fillet_2.html', help='Path to the HTML file')
    args = parser.parse_args()
    html_file = args.html_file
    output_json_file = 'output.json'

    html_table_to_json(html_file, output_json_file)
