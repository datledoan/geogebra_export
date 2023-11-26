import pandas as pd
import json
import re
import os
import argparse

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

# Filter the features using in "Definition" field of "List"
def filter(output_json_file,output_filtered_json):
    with open(output_json_file, 'r') as json_file:
        json_data = json.load(json_file)

    # Search for the features using in "Definition" field of "List"
    list_values = []
    for row in json_data:
        if 'List' in row.get('Name', ''):
            definition_values = re.findall(r'\b\w\b', row.get('Definition', ''))
            list_values.extend(definition_values)
    

    
    # Check if the name of the row contains "Segment", "Arc" or "Point"
    name_pattern = re.compile(r'(Segment|Arc|Point)\s+([a-zA-Z])', re.IGNORECASE)

    # Filter the rows with the name containing "Segment", "Arc" or "Point" and the value in "Definition" field is in the list_values
    filtered_rows = [row for row in json_data if name_pattern.search(row.get('Name', '')) and name_pattern.search(row.get('Name', '')).group(2) in list_values]

    for i, item in enumerate(filtered_rows):
        item['id'] = i + 1 
    
    with open(output_filtered_json, 'w') as output_file:
        json.dump(filtered_rows, output_file, indent=2)


# Add "startid" and "endid" to each segment and arc
def add_start_end_ids(output_filtered_json):
    
    with open(output_filtered_json, 'r') as json_file:
        data = json.load(json_file)

    # dictionary key: name, value: id
    name_to_id = {item['Name']: item['id'] for item in data}
    
    
    for item in data:
        if item['Name'].startswith('Segment'):
            # search for start_id and end_id
            start_name, end_name = item['Definition'].replace('Segment(', '').replace(')', '').split(', ')
            start_id = name_to_id['Point ' + start_name]
            end_id = name_to_id['Point ' + end_name]

            
            item['startid'] = start_id
            item['endid'] = end_id
        
        if item['Name'].startswith('Arc'):
            # search for start_id and end_id
            center_name,start_name, end_name = item['Definition'].replace('Arc(', '').replace(')', '').split(', ')
            start_id = name_to_id['Point ' + start_name]
            end_id = name_to_id['Point ' + end_name]

            
            item['startid'] = start_id
            item['endid'] = end_id

    
    with open(output_filtered_json, 'w') as json_file:
        json.dump(data, json_file, indent=2)


# Format data to GeoJSON
def convert_to_feature(point_data):
    name = point_data.get('Name', '')
    value = point_data.get('Value', '')
    id_counter = point_data.get('id', 0) + 1
    #Point
    if name.startswith("Point"):
        
        coordinates = [float(coord) for coord in re.findall(r'-?\d+\.\d+', value)]

        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": coordinates
            },
            "properties": {
                "id": id_counter,
                "frame": "map"
            }
        }
        return feature
    #Segment
    elif name.startswith("Segment"):
        
        length = [float(coord) for coord in re.findall(r'-?\d+\.\d+', value)]
        start_id = point_data.get('startid', 0)
        end_id = point_data.get('endid', 0)
        # Tạo cấu trúc mới
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Segment",
                "length": length
            },
            "properties": {
                "id": id_counter,
                "frame": "map",
                "startid": start_id,
                "endid": end_id
            }
        }
    #Circlearc
    elif name.startswith("Arc"):
        length = [float(coord) for coord in re.findall(r'-?\d+\.\d+', value)]
        start_id = point_data.get('startid', 0)
        end_id = point_data.get('endid', 0)
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Arc",
                "length": length
            },
            "properties": {
                "id": id_counter,
                "frame": "map",
                "startid": start_id,
                "endid": end_id
            }
        }
        return feature
    return None

def graph_json(output_filtered_json,graph_file_path):
    with open(output_filtered_json, 'r') as json_file:
        original_data = json.load(json_file)

    # Chuyển đổi dữ liệu
    features = []

    for data_point in original_data:
        feature = convert_to_feature(data_point)
        if feature:
            features.append(feature)

    # Write graph to json file
    with open(graph_file_path, 'w') as output_json_file:
        json.dump(features, output_json_file, indent=2)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Convert HTML table to graph in JSON')
    parser.add_argument('--html_file', type=str, default='map1.html', help='Path to the HTML file')
    parser.add_argument('--graph_file_path', type=str, default='graph.json', help='Path to the graph JSON file')
    parser.add_argument('--delete_unnecessary_files', type=bool, default=True, help='Delete unnecessary files')
    args = parser.parse_args()


    html_file = args.html_file
    output_json_file = 'output.json'
    output_filtered_json = "filtered_feature.json"
    graph_file_path = args.graph_file_path

    html_table_to_json(html_file, output_json_file)
    filter(output_json_file,output_filtered_json)
    add_start_end_ids(output_filtered_json)
    graph_json(output_filtered_json,graph_file_path)

    if args.delete_unnecessary_files:
        os.remove(output_json_file)
        os.remove(output_filtered_json)