import zipfile
import xml.etree.ElementTree as ET

# Đường dẫn đến tệp ZIP và tên tệp XML bạn muốn chỉnh sửa
zip_file_path = 'duong_dan_den_tep_zip.zip'
xml_file_name = 'ten_file.xml'

# Giải nén tệp ZIP
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    # Đọc nội dung của tệp XML từ tệp ZIP
    xml_content = zip_ref.read(xml_file_name)

    # Chuyển đổi nội dung XML thành đối tượng ElementTree
    root = ET.fromstring(xml_content)

    # Thực hiện các thay đổi cần thiết trong cây XML
    # Ví dụ: Đổi giá trị của một phần tử
    for element in root.iter('ElementName'):
        element.text = 'NewValue'

# Nén lại tệp ZIP với nội dung XML đã được chỉnh sửa
with zipfile.ZipFile(zip_file_path, 'a') as zip_ref:
    # Xóa tệp XML cũ khỏi tệp ZIP
    zip_ref.extractall('temporary_extracted_folder')

    # Ghi tệp XML mới vào tệp ZIP
    zip_ref.write('temporary_extracted_folder/' + xml_file_name, xml_file_name)

# Xóa thư mục tạm thời
import shutil
shutil.rmtree('temporary_extracted_folder')
