from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
from pymongo import MongoClient
import uuid
app = Flask(__name__)
CORS(app)

# Connect MongoDB
client = MongoClient("mongodb+srv://muralispc117:Murali1234@cluster0.v9gz99u.mongodb.net/")
db = client["mydb"]
collection = db["users"]

import os

@app.route("/uploadnewplace", methods=["POST"])
def upload_newplace():

    file = request.files.get('image')
    

    if file and file.filename:
        filename = str(uuid.uuid4()) + "_" + file.filename
        print(filename)
        file.save(os.path.join('static/images', filename))
    else:
        filename = None
       

    data = {
        'state': request.form.get('state'),
        'location': request.form.get('location'),
        'image': filename,
        'days': request.form.get('days'),
        
        'cost': int(request.form.get('cost', 0)),
        'seats': int(request.form.get('seats', 0)),
        'climate': request.form.get('climate')
    }

    collection.insert_one(data)

    destinaton = list(collection.find({}, {'_id': False}))

    return render_template('index.html', destinaton=destinaton)

@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)