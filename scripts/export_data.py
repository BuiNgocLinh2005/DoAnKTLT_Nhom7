import os
import json
from pymongo import MongoClient

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MuseumDB"]
collection = db["museums"]

# Thư mục để lưu JSON export
export_folder = "database/exported_data"
os.makedirs(export_folder, exist_ok=True)

# Xuất dữ liệu từng bảo tàng
for museum in collection.find():
    museum_name = museum["name"]
    file_path = os.path.join(export_folder, f"{museum_name}.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(museum, f, ensure_ascii=False, indent=4)
    
    print(f"✅ Đã xuất: {museum_name}")

print("✅ Hoàn thành export dữ liệu từ MongoDB!")
