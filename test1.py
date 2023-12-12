import re
import json

# Đọc dữ liệu từ tệp JSON
with open('output.json', 'r') as json_file:
    data_list = json.load(json_file)

# Tạo một dictionary để lưu trữ kết quả


# Hàm để thêm một mục vào dictionary kết quả
def add_to_result(data,result_dict):
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


result_dict = {}
# Duyệt qua danh sách dữ liệu và thêm từng mục vào dictionary kết quả
for data in data_list:
    add_to_result(data,result_dict)

# In ra kết quả
print(result_dict)
