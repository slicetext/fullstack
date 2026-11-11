import psycopg
# Load db
import os
from dotenv import load_dotenv
import requests

load_dotenv()

password: str = os.getenv("PASSWORD")

conn_str: str = f"postgresql://project_user:{password}@localhost:5432/project_db"

conn = psycopg.connect(conn_str)
cur = conn.cursor()

from flask import Flask, request, send_from_directory, render_template, url_for
from flask_cors import CORS
from flask_login import (LoginManager, UserMixin, current_user, login_required, login_user, logout_user)
from werkzeug.security import check_password_hash

app = Flask(__name__)
# CORS(app, supports_credentials = True, origins=["http://127.0.0.1:5000", "http://192.168.110.146:8000", "http://192.168.111.8:5000"])
CORS(app,resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:8000","http://192.168.110.146:8000"],
        "supports_credentials": True
        }
    })
# CORS(app)
app.secret_key = os.environ["SECRET_KEY"]


login_manager = LoginManager()
login_manager.init_app(app)
CORS(app)

class User(UserMixin):
    def __init__(self, user_id, username, admin):
        self.id = user_id
        self.username = username
        self.admin = admin

@login_manager.user_loader
def load_user(owner_id):
    cur.execute(
            # SUPER UNSAFE!! CAN BE INJECTED INTO!!! FIX!!!!!!!
            f"SELECT owner_id, name, admin FROM owner WHERE owner_id = {owner_id}"
    )
    row = cur.fetchone()
    if (row):
        return User(row[0], row[1], row[2])

@login_manager.unauthorized_handler
def unauthorized():
    return {"error": "You must log in"}, 401

@app.route("/")
def index():
     # return send_from_directory(app.static_folder, 'index.html')
     return render_template('index.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or ("username" not in data or "password" not in data):
        return {"error": "username and password are required"}, 400

    # SUPER UNSAFE!! CAN BE INJECTED INTO!!! FIX!!!!!!!
    cur.execute(f"SELECT owner_id, name, admin, password FROM owner WHERE name = '{data['username']}'")
    row = cur.fetchone()

    if row is None or not check_password_hash(row[3], data["password"]):
        return {"error": "Wrong username or password"}, 401

    user = User(row[0], row[1], row[2])
    login_user(user, remember=True)
    return {"message": f"Logged in as {row[1]}, Admin: {row[2]}", "home": url_for('index')}#, user: user}

@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return {"message": "Logged out"}

@app.route("/api/search")
def search():
    print(current_user)
    query = request.args.get("q", "")
    cur.execute(
            # SUPER UNSAFE!! CAN BE INJECTED INTO!!! FIX!!!!!!!
            f"SELECT ip.ip_address, owner.name, ip.description FROM ip JOIN owner ON ip.owner_id = owner.owner_id WHERE ip_address LIKE '%{query}%'"
    )
    return cur.fetchall()
    return

@app.route("/api/user_addresses")
@login_required
def user_addresses():
    cur.execute(
            f"SELECT * FROM ip WHERE owner_id = {current_user.id};"
    )
    return cur.fetchall()

@app.route("/api/remove_address", methods=["POST"])
@login_required
def remove_address():
    data = request.get_json()
    if not data or ("address" not in data):
        return {"error": "address required"}
    
    cur.execute(f"DELETE FROM ip WHERE owner_id = '{current_user.id}' AND ip_address = '{data['address']}';")
    return "good"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

cur.close()
conn.close()


