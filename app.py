from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Tạo bảng nếu chưa có
with get_db_connection() as conn:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            museum_name TEXT,
            username TEXT,
            comment TEXT,
            timestamp TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            museum_name TEXT,
            username TEXT,
            rating INTEGER,
            comment TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get("email")
    password = generate_password_hash(data.get("password"))
    
    try:
        conn = get_db_connection()
        conn.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "Đăng ký thành công!"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email đã tồn tại!"}), 400

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    conn = get_db_connection()
    user = conn.execute("SELECT password FROM users WHERE email = ?", (email,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user["password"], password):
        session['user'] = email
        return jsonify({"redirect": url_for('home')})  # Chuyển hướng về home
    return jsonify({"error": "Sai email hoặc mật khẩu!"}), 401

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))  # Chuyển hướng về trang chủ sau khi đăng xuất

@app.route("/reviews")
def reviews():
    return render_template("review.html")

@app.route("/comments/<museum_name>", methods=["GET"])
def get_comments(museum_name):
    conn = get_db_connection()
    comments = conn.execute("SELECT username, comment, timestamp FROM comments WHERE museum_name = ? ORDER BY timestamp DESC", (museum_name,)).fetchall()
    conn.close()
    
    return jsonify([{ "username": c["username"], "comment": c["comment"], "timestamp": c["timestamp"] } for c in comments])

@app.route("/comments", methods=["GET"])
def comment_page():
    return render_template("comment.html")

@app.route("/comments", methods=["POST"])
def add_comment():
    if 'user' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để bình luận!"}), 401
    
    data = request.json  # Nhận dữ liệu JSON thay vì request.form
    museum_name = data.get("museum_name", "Tên bảo tàng mặc định")
    username = session.get('user')
    comment = data.get("comment", "").strip()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not comment:
        return jsonify({"error": "Nội dung bình luận không được để trống!"}), 400
    
    conn = get_db_connection()
    conn.execute("INSERT INTO comments (museum_name, username, comment, timestamp) VALUES (?, ?, ?, ?)", (museum_name, username, comment, timestamp))
    conn.commit()
    conn.close()

    return jsonify({"message": "Bình luận đã được ghi nhận!"}), 201


@app.route("/reviews", methods=["POST"])
def add_review():
    if 'user' not in session:
        return jsonify({"error": "Bạn cần đăng nhập để đánh giá!"}), 401
    
    data = request.json
    museum_name = data.get("museum_name")
    username = session['user']
    rating = data.get("rating")
    comment = data.get("comment")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not museum_name or not rating:
        return jsonify({"error": "Thiếu thông tin đánh giá!"}), 400
    
    conn = get_db_connection()
    conn.execute("INSERT INTO reviews (museum_name, username, rating, comment, timestamp) VALUES (?, ?, ?, ?, ?)", (museum_name, username, rating, comment, timestamp))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Đánh giá đã được ghi nhận!"}), 201

@app.route("/reviews/<museum_name>", methods=["GET"])
def get_reviews(museum_name):
    conn = get_db_connection()
    reviews = conn.execute("SELECT username, rating, comment, timestamp FROM reviews WHERE museum_name = ? ORDER BY timestamp DESC", (museum_name,)).fetchall()
    conn.close()
    
    return jsonify([{ "username": r["username"], "rating": r["rating"], "comment": r["comment"], "timestamp": r["timestamp"] } for r in reviews])
@app.route("/check-login")
def check_login():
    return jsonify({"logged_in": 'user' in session})


if __name__ == "__main__":
    app.run(debug=True)