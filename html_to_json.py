import pandas as pd
import json
import re

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
    target_table.to_json(json_filename, orient='records', lines=False)


def filter(output_json_file,output_filtered_json):
    # Đọc từ tệp JSON
    with open(output_json_file, 'r') as json_file:
        json_data = json.load(json_file)

    # Tìm giá trị từ trường "Definition" của các hàng có "Name" chứa "List"
    list_values = []
    for row in json_data:
        if 'List' in row.get('Name', ''):
            definition_values = re.findall(r'\b\w\b', row.get('Definition', ''))
            list_values.extend(definition_values)
    

    
    # Biểu thức chính quy để kiểm tra "Name"
    name_pattern = re.compile(r'(Segment|Arc|Point)\s+([a-zA-Z])', re.IGNORECASE)

    # Lọc và in ra các dòng thỏa mãn điều kiện
    filtered_rows = [row for row in json_data if name_pattern.search(row.get('Name', '')) and name_pattern.search(row.get('Name', '')).group(2) in list_values]

    print("result")
    # In ra kết quả
    
    with open(output_filtered_json, 'w') as output_file:
        json.dump(filtered_rows, output_file, indent=2)

# Example usage
html_file = 'map1.html'  # Replace with the path to your HTML file
output_json_file = 'output.json'
output_filtered_json = "filtered_feature.json"

html_table_to_json(html_file, output_json_file)
filter(output_json_file,output_filtered_json)