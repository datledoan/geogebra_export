import json

# Dữ liệu ban đầu
data = [
    {
        "Name": "Arc c",
        "Definition": "fillet13(D, B, E)",
        "Value": "c = 0.9024890814",
        "id": 10
    },
    {
        "Name": "Point F",
        "Definition": "fillet13(D, B, E)",
        "Value": "F = (5.5, 7.5745423936)",
        "id": 11
    },
    {
        "Name": "Point G",
        "Definition": "fillet13(D, B, E)",
        "Value": "G = (6.0745423936, 7)",
        "id": 12
    },
    {
        "Name": "Point H",
        "Definition": "fillet13(D, B, E)",
        "Value": "H = (6.0745423936, 7.5745423936)",
        "id": 13
    },
    {
        "Name": "Arc v",
        "Definition": "fillet13(V, W, Z)",
        "Value": "v = 1.23456789",
        "id": 14
    },
    {
        "Name": "Point W",
        "Definition": "fillet13(V, W, Z)",
        "Value": "W = (3.0, 4.0)",
        "id": 15
    },
    {
        "Name": "Point X",
        "Definition": "fillet13(V, W, Z)",
        "Value": "X = (2.5, 4.5)",
        "id": 16
    },
    {
        "Name": "Point Y",
        "Definition": "fillet13(V, W, Z)",
        "Value": "Y = (3.5, 5.5)",
        "id": 17
    }
]

# Tìm các điểm có "Definition" là "fillet13(D, B, E)" hoặc "fillet13(V, W, Z)"
arc_data = [item for item in data if "fillet13" in item.get("Definition")]
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
