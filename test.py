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
        start_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 1)
        end_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 2)
        origin_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 3)

        feature = {
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

        features.append(feature)

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

print("Chuyển đổi hoàn tất. Dữ liệu được xuất ra file 'output.json'")
