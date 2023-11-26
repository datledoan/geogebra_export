import json

def add_start_end_ids(json_file_path):
    # Đọc file JSON
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Tạo một từ điển để ánh xạ tên điểm (key) với id (value)
    name_to_id = {item['Name']: item['id'] for item in data}
    
    # Thêm trường "startid" và "endid" cho mỗi đoạn thẳng
    for item in data:
        if item['Definition'] and item['Name'].startswith('Segment'):
            # Tìm id của điểm đầu và cuối
            start_name, end_name = item['Definition'].replace('Segment(', '').replace(')', '').split(', ')
            start_id = name_to_id['Point ' + start_name]
            end_id = name_to_id['Point ' + end_name]

            # Thêm trường "startid" và "endid"
            item['startid'] = start_id
            item['endid'] = end_id

    # Ghi lại dữ liệu đã cập nhật vào file JSON
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=2)

# Thay 'input.json' bằng đường dẫn đến file JSON của bạn
add_start_end_ids('filtered_feature.json')
