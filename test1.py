import json
import re

def extract_coordinates(json_file_path):
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

        for item in data:
            name = item.get('Name', '')
            value = item.get('Value', '')

            if name and value:
                # Sử dụng biểu thức chính quy để trích xuất tọa độ từ giá trị "Value"
                match = re.search(r'\((-?\d+\.\d+), (-?\d+\.\d+)\)', value)
                if match:
                    x_coordinate, y_coordinate = match.groups()
                    print(f"{name}: ({x_coordinate}, {y_coordinate})")

# Thay 'input.json' bằng đường dẫn đến file JSON của bạn
extract_coordinates('test.json')