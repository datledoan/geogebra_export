import json
import pandas as pd


def html_table_to_json(html_filename, json_filename):
    # Read HTML file into a list of DataFrames
    tables = pd.read_html(html_filename)

    if not tables:
        print("No tables found in the HTML file.")
        return

    # Assuming the first table is the target table
    target_table = tables[0]

    # Save the table to a JSON file
    target_table.to_json(json_filename, orient='records', lines=False,indent=2,index=True)

    with open(json_filename, 'r') as json_file:
        data = json.load(json_file)
    for i, item in enumerate(data):
        item['id'] = i + 1
    with open(json_filename, 'w') as output_file:
        json.dump(data, output_file, indent=2)
        
        

html_table_to_json('test_fillet.html', 'test.json')

# Dữ liệu ban đầu
with open("test.json", "r") as infile:
    data = json.load(infile)
print(data)
# Tìm các điểm có "Definition" là "fillet13(D, B, E)" hoặc "fillet13(V, W, Z)"
arc_data = [item for item in data if "fillet" in item.get("Definition")]
print("data:=================")
print(arc_data)
# Tạo định dạng mới
features = []
for arc in arc_data:
    if "Arc" in arc.get("Name"):
      print(arc.get("id"))
      start_point = next(item for item in arc_data if item.get("id") == arc.get("id") + 1)
      end_point = next(item for item in arc_data if item.get("id") == arc.get("id") + 2)
      origin_point = next(item for item in arc_data if item.get("id") == arc.get("id") + 3)

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

# Xuất ra file JSON mới
output_data = {
    "type": "FeatureCollection",
    "features": features
}

print(features)

# with open("output.json", "w") as outfile:
#     json.dump(output_data, outfile, indent=2)

print("Chuyển đổi hoàn tất. Dữ liệu được xuất ra file 'output.json'")
