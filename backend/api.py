from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS  # Cho phép frontend gọi API

app = Flask(__name__)
CORS(app)  # Cho phép truy cập từ frontend

# Kết nối MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["MuseumDB"]
collection = db["museums"]

@app.route("/museum/<museum_id>", methods=["GET"])
def get_museum(museum_id):
    museum = collection.find_one({"id": museum_id}, {"_id": 0})  # Lấy dữ liệu trừ _id
    if museum:
        return jsonify(museum)
    else:
        return jsonify({"error": "Bảo tàng không tồn tại"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)


