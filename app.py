from flask import Flask, request, jsonify,render_template,redirect,url_for
from flask_cors import CORS
from pymongo import MongoClient
import uuid
from bson.objectid import ObjectId
app = Flask(__name__)
CORS(app)

# Connect MongoDB
client = MongoClient("mongodb+srv://muralispc117:Murali1234@cluster0.v9gz99u.mongodb.net/")
db = client["mydb"]
collection = db["holidaytours"]

import os

@app.route("/uploadnewplace", methods=["POST"])
def upload_newplace():

    file = request.files.get('image')
    
    if file and file.filename:
        filename = str(file.filename)
       
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
    return redirect(url_for('home')) 

@app.route("/deleteplace/<id>")
def deleteplace(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('home')) 

@app.route("/updateinfo/<id>")
def updateinfo(id):
    newinfo = collection.find_one({'_id':ObjectId(id)})
    return render_template('update.html', newinfo=newinfo)

@app.route("/updateplace/<id>", methods = ["POST",'GET'])
def update(id):
    file = request.files.get('image')

    if file and file.filename:
        filename = str(file.filename)
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
    collection.update_one({'_id':ObjectId(id)}, {'$set': data})
    return redirect(url_for('home'))

@app.route("/")
def home():
    destinaton = list(collection.find({}))
    return render_template('index.html', destinaton=destinaton)
   
if __name__ == "__main__":
    app.run(debug=True)