from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)
"""
from pymongo import MongoClient

client = MongoClient("mongodb+srv://yourUser:yourPassword@cluster0.xxxxx.mongodb.net/")

db = client["mydb"]          # DB name (will be created automatically)
collection = db["users"]    # Collection name
mongodb+srv://muralispc117:Murali1234@cluster0.v9gz99u.mongodb.net/
"""
# Connect MongoDB
client = MongoClient("mongodb+srv://muralispc117:Murali1234@cluster0.v9gz99u.mongodb.net/")
db = client["mydb"]
collection = db["users"]

@app.route("/save", methods=["POST"])
def save_data():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Data saved successfully"})

@app.route("/users", methods=["GET"])
def get_users():
    users = list(collection.find({}, {"_id": 0}))
    return jsonify(users)

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True) 