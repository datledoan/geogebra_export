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
    

    
    # Check if the name of the row contains "Segment", "Arc"
    name_pattern = re.compile(r'(Segment|Arc)\s+([a-zA-Z])', re.IGNORECASE)

    # Filter the rows with the name containing "Segment", "Arc" and the value in "Definition" field is in the list_values
    filtered_rows = [row for row in json_data if name_pattern.search(row.get('Name', '')) and name_pattern.search(row.get('Name', '')).group(2) in list_values or 'Point' in row.get('Name', '')]

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
            origin_name,start_name, end_name = item['Definition'].replace('CircularArc(', '').replace(')', '').split(', ')
            start_id = name_to_id['Point ' + start_name]
            end_id = name_to_id['Point ' + end_name]
            origin_id = name_to_id['Point ' + origin_name]

            
            item['startid'] = start_id
            item['endid'] = end_id
            item['originid'] = origin_id

    
    with open(output_filtered_json, 'w') as json_file:
        json.dump(data, json_file, indent=2)

#read size of image
def read_pgm_dimensions(pgm_file_path):
    with open(pgm_file_path, 'rb') as file:
        # skip first line
        file.readline()
        
        # read second line
        size_line = file.readline().decode('utf-8').split()
        width, height = map(int, size_line)

    return width

#read resolution and origin in map_info.yaml
def read_yaml(yaml_file_path):
    with open(yaml_file_path, 'r') as file:
        data = yaml.safe_load(file)
        resolution = data.get('resolution')
        origin = data.get('origin')
    return resolution, origin


# Format data to GeoJSON
def convert_to_feature(point_data, origin, ratio):
    name = point_data.get('Name', '')
    value = point_data.get('Value', '')
    id_counter = point_data.get('id', 0) 
    


    #Point
    if name.startswith("Point"):
        
        coordinates = re.findall(r'-?\d+(?:\.\d+)?', value)
        x=0
        y=0
        if len(coordinates) >= 2:
            x_coordinate, y_coordinate = map(float, coordinates[:2])
            x = float(x_coordinate) / ratio + origin[0]
            y = float(y_coordinate) / ratio + origin[1]
        else:
            print("Error: Point coordinates must be 2D, coordinates will be set to (0,0)")
        #print(x,y)
        #print(f"{name}: ({x_coordinate}, {y_coordinate})")
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [x,y]
            },
            "properties": {
                "id": id_counter,
                "frame": "map"
            }
        }
        return feature
    #Segment
    elif name.startswith("Segment"):
        
        length = [float(coord) for coord in re.findall(r'-?\d+(?:\.\d+)?', value)]

        length = length[0] / ratio

        start_id = point_data.get('startid', 0)
        end_id = point_data.get('endid', 0)

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
        return feature
    #Circlearc
    elif name.startswith("Arc"):
        length = [float(coord) for coord in re.findall(r'-?\d+(?:\.\d+)?', value)]
        start_id = point_data.get('startid', 0)
        end_id = point_data.get('endid', 0)
        origin_id = point_data.get('originid',0)
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
                "endid": end_id,
                "originid": origin_id
            }
        }
        return feature
    return None

def graph_json(output_filtered_json,graph_file_path, pgm_file_path, yaml_file_path):

    # Read size of image
    width = read_pgm_dimensions(pgm_file_path)
    #read resolution and origin in map_info.yaml
    resolution, origin = read_yaml(yaml_file_path)


    with open(output_filtered_json, 'r') as json_file:
        original_data = json.load(json_file)

    for item in original_data:
        if item['Name'] == 'Point B':
            x = float(item['Value'].replace('B = (', '').replace(')', '').split(', ')[0])
            break
    
    #ratio between geogebra and real world
    ratio = x / (width*resolution)

            
    features = []

    for data_point in original_data:
        feature = convert_to_feature(data_point, origin, ratio)
        if feature:
            features.append(feature)

    # Write graph to json file
    with open(graph_file_path, 'w') as output_json_file:
        json.dump(features, output_json_file, indent=2)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Convert HTML table to graph in JSON')
    parser.add_argument('--html_file', type=str, default='map1.html', help='Path to the HTML file')
    parser.add_argument('--graph_file_path', type=str, default='graph.json', help='Path to the graph JSON file')
    parser.add_argument('--delete_unnecessary_files', type=bool, default=False, help='Delete unnecessary files')
    parser.add_argument('--pgm_file_path', type=str, default='map.pgm', help='Path to the pgm file')
    parser.add_argument('--yaml_file_path', type=str, default='map_info.yaml', help='Path to the yaml file')
    args = parser.parse_args()


    html_file = args.html_file
    output_json_file = 'output.json'
    output_filtered_json = "filtered_feature.json"
    graph_file_path = args.graph_file_path
    pgm_file_path = args.pgm_file_path
    yaml_file_path = args.yaml_file_path

    html_table_to_json(html_file, output_json_file)
    filter(output_json_file,output_filtered_json)
    add_start_end_ids(output_filtered_json)
    graph_json(output_filtered_json,graph_file_path, pgm_file_path, yaml_file_path)

    if args.delete_unnecessary_files:
        os.remove(output_json_file)
        os.remove(output_filtered_json)