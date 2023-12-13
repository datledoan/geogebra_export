import pandas as pd
import json
import re
import os
import argparse
import yaml


def dict_name_id(data,result_dict):
    # Lấy giá trị từ trường "Name"
    name = data.get('Name', '')

    # Tìm tất cả các ký tự và số trước dấu ngoặc
    match = re.match(r'([^()]+)', name)

    # Kiểm tra xem có kết quả từ việc tìm kiếm không
    if match:
        # Lấy phần match đầu tiên (đã loại bỏ dấu ngoặc)
        key = match.group(1).strip()

        # Lấy giá trị từ trường "id"
        value = data.get('id')

        # Thêm mục vào dictionary kết quả
        result_dict[key] = value

def process_data(data):
    
    features = []
    
    name_to_id = {}
    for item in data:
      dict_name_id(item,name_to_id)

    print(name_to_id)

    arc_data = [item for item in data if item.get("Definition") and "fillet" in item.get("Definition")]

    for arc in arc_data:
      if arc.get("Name").startswith("Arc"):

        start_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 2)
        end_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 1)
        origin_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 3)
        
        first_name, second_name, third_name = item['Definition'].replace('fillet(', '').replace(')', '').split(', ')
        first_id = name_to_id['Point ' + first_name]
        second_id = name_to_id['Point ' + second_name]
        third_id = name_to_id['Point ' + third_name]

        segment_1 = next(item for item in arc_data if item.get("id") == arc.get("id") + 1)
        segment_2 = next(item for item in arc_data if item.get("id") == arc.get("id") + 2)    
        segment_3 = next(item for item in arc_data if item.get("id") == arc.get("id") + 3)
        segment_4 = next(item for item in arc_data if item.get("id") == arc.get("id") + 4)

        feature_arc = {
            "type": "Feature",
            "geometry": {
                "type": "Arc"
            },
            "properties": {
                "id": arc["id"],
                "startid": start_point["id"],
                "endid": end_point["id"],
                "originid": origin_point["id"],
                "frame": "map"
            }
        }

        features.append(feature_arc)

        feature_segment_1 = {
            "type": "Feature",
            "geometry": {
                "type": "Segment"
            },
            "properties": {
                "id": segment_1["id"],
                "startid": first_id,
                "endid": start_point["id"],
                "frame": "map"
            }
        }

        features.append(feature_segment_1)

        feature_segment_2 = {
            "type": "Feature",
            "geometry": {
                "type": "Segment"
            },
            "properties": {
                "id": segment_2["id"],
                "startid": start_point["id"],
                "endid": second_id,
                "frame": "map"
            }
        }

        features.append(feature_segment_2)

        feature_segment_3 = {
            "type": "Feature",
            "geometry": {
                "type": "Segment"
            },
            "properties": {
                "id": segment_3["id"],
                "startid": second_id,
                "endid": end_point["id"],
                "frame": "map"
            }
        }

        features.append(feature_segment_3)

        feature_segment_4 = {
            "type": "Feature",
            "geometry": {
                "type": "Segment"
            },
            "properties": {
                "id": segment_4["id"],
                "startid": end_point["id"],
                "endid": third_id,
                "frame": "map"
            }
        }

        features.append(feature_segment_4)
        


    return features

# Đọc dữ liệu từ tệp JSON
with open("test.json", "r") as infile:
    data = json.load(infile)

# Xử lý dữ liệu và tạo định dạng mới
new_features = process_data(data)

# Xuất ra file JSON mới
output_data = {
    "type": "FeatureCollection",
    "features": new_features
}

print(new_features)

# with open("output.json", "w") as outfile:
#     json.dump(output_data, outfile, indent=2)

