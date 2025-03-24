import json
import pymongo

# Kết nối MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["museum_db"]
collection = db["museums"]

# Đọc dữ liệu từ JSON
with open("database/museums_data.json", "r", encoding="utf-8") as f:
    museums = json.load(f)

# Insert vào MongoDB
collection.insert_many(museums)
print("✅ Dữ liệu đã được insert vào MongoDB")

