import os
import json
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MuseumDB"]
collection = db["museums"]

# Duyệt tất cả các file JSON trong thư mục museums_data
data_folder = "database/museums_data"

for filename in os.listdir(data_folder):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            museum_data = json.load(f)
            museum_name = museum_data.get("name", "Unknown Museum")
            collection.insert_one(museum_data)
            print(f"✅ Đã insert: {museum_name}")

print("✅ Hoàn thành insert dữ liệu vào MongoDB!")
