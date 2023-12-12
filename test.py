import json

# Dữ liệu ban đầu
data = [
  {
    "Name": "Point P",
    "Definition": "fillet(D, F, E)",
    "Value": "P = (13.3, 9.1)",
    "id": 34
  },
  {
    "Name": "Point Q",
    "Definition": "fillet(D, F, E)",
    "Value": "Q = (15.23, 9.11)",
    "id": 35
  },
  {
    "Name": "Point R",
    "Definition": "fillet(D, F, E)",
    "Value": "R = (13.29, 11.04)",
    "id": 36
  },
  {
    "Name": "Arc c1",
    "Definition": "fillet(D, F, E)",
    "Value": "c1 = 3.05",
    "id": 37
  },
  {
    "Name": "Segment b",
    "Definition": "fillet(D, F, E)",
    "Value": "b = 3.53",
    "id": 38
  },
  {
    "Name": "Segment f1",
    "Definition": "fillet(D, F, E)",
    "Value": "f1 = 1.94",
    "id": 39
  },
  {
    "Name": "Segment g1",
    "Definition": "fillet(D, F, E)",
    "Value": "g1 = 1.94",
    "id": 40
  },
  {
    "Name": "Segment h1",
    "Definition": "fillet(D, F, E)",
    "Value": "h1 = 5.31",
    "id": 41
  }
]

# Tìm các điểm có "Definition" là "fillet13(D, B, E)" hoặc "fillet13(V, W, Z)"
arc_data = [item for item in data if "fillet" in item.get("Definition")]
print(arc_data)
# Tạo định dạng mới
features = []
for arc in arc_data:
    if "Arc" in arc.get("Name"):
      print(arc.get("id"))
      start_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 2)
      end_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 3)
      origin_point = next(item for item in arc_data if item.get("id") == arc.get("id") - 1)

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
