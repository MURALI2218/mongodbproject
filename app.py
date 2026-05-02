from flask import Flask, request, jsonify,render_template,redirect,url_for,session
from flask_cors import CORS
from pymongo import MongoClient

from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)

app.secret_key = "your_secret_key"

# Connect MongoDB
client = MongoClient("mongodb+srv://muralispc117:Murali1234@cluster0.v9gz99u.mongodb.net/")
db = client["mydb"]
collection = db["holidaytours"]
users = db["users"]
booking = db["booking"]

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


@app.route("/index")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    else:
        destinaton = list(collection.find({}))
        
        return render_template('index.html', destinaton=destinaton, urname = session.get('username'),role=session.get('role'))


@app.route('/')
@app.route('/login')
def login():
    session.clear()
    return render_template("login.html")

# @app.route('/logout')
# def logout(): 
#     return redirect(url_for('login'))
#     return render_template("login.html")
#     return redirect(url_for('loginpage'))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/cerds' , methods=['POST'])
def cerds():
    logusername = request.form.get('username')
    userpassword = request.form.get('password')

    user = users.find_one({
        "username" : logusername,
        "password" : userpassword
    })

     
    if user:
        # store session
        session['username'] = user['username']
        session['role'] = user['role']
        
       
       
        return redirect(url_for('home'))     
    return " invalid credentials"

@app.route('/signupcerds', methods = ['POST'])
def signupcerds():
    data = {
        'username':request.form.get('username'),
        'password':request.form.get('password'),
        'role':'user'
    }
    users.insert_one(data)
    return redirect('/')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/userbooking/<id>', methods = ['GET'])
def userbooking(id):
    userdetails = collection.find_one({'_id':ObjectId(id)})
    print(userdetails)
    return render_template('booking.html', userdetails = userdetails)

@app.route('/userbookingdata', methods = ["POST"])
def userbookingdata():
    destination_id = request.form.get("destination")
    destination = collection.find_one({'_id':ObjectId(destination_id)})

    userid = users.find_one({ 'username' : session['username']})
    print(userid)
    data = {
        'userid' : userid.get('_id'),
        'name' : request.form.get('name'),
        'phonenumber':int(request.form.get('phonenumber')),
         'peoplecount':int(request.form.get('peoplecount')),
         'email' : request.form.get('email'),
         'userdate':request.form.get('date'),
        'userstate':destination.get('state'),
        'userplace':destination.get('location'),
        'userdays': destination.get('days'),
        'userclimate' : destination.get('climate')
    }
    
    booking.insert_one(data)
   
    return redirect(url_for('home'))

@app.route('/allbookingsforadmin')
def allbookingsforadmin():
    if session['role'] == 'admin':
        data= booking.find({})
        return render_template('userbookings.html', data=data, role = session.get('role'))
    else:
        
        data= booking.find({'userid': ObjectId("69f3861177f10e8237861c6d")})
        
        return render_template('userbookings.html', data=data, role = session.get('role'))
        

if __name__ == "__main__":
    app.run(debug=True)