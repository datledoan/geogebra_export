import json

# Đọc dữ liệu từ tệp JSON
with open("test.json", "r") as infile:
    data = json.load(infile)

# Tìm các điểm có "Definition" là "fillet13(D, B, E)" hoặc "fillet13(V, W, Z)"
arc_data = [item for item in data if "fillet13" in item.get("Definition")]

# Tạo định dạng mới
features = []
for arc in arc_data:
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

with open("output.json", "w") as outfile:
    json.dump(output_data, outfile, indent=2)

print("Chuyển đổi hoàn tất. Dữ liệu được xuất ra file 'output.json'")
