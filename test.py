import json
import re

def convert_to_feature(point_data):
    name = point_data.get('Name', '')
    value = point_data.get('Value', '')
    id_counter = point_data.get('id', 0)

    if name.startswith("Point"):
        # Lấy giá trị từ trường "Value"
        coordinates = [float(coord) for coord in re.findall(r'-?\d+\.\d+', value)]

        # Tạo cấu trúc mới
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
    elif name.startswith("Segment"):
        # Lấycoordinates giá trị từ trường "Value"
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
    elif name.startswith("Arc"):
        length = [float(coord) for coord in re.findall(r'-?\d+\.\d+', value)]
        start_id = point_data.get('startid', 0)
        end_id = point_data.get('endid', 0)
        # Tạo cấu trúc mới
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

# Đọc từ tệp JSON
with open('filtered_feature.json', 'r') as json_file:
    original_data = json.load(json_file)

# Chuyển đổi dữ liệu
features = []

for data_point in original_data:
    feature = convert_to_feature(data_point)
    if feature:
        features.append(feature)

# Ghi ra tệp JSON mới
with open('path_to_your_output_json_file.json', 'w') as output_json_file:
    json.dump(features, output_json_file, indent=2)