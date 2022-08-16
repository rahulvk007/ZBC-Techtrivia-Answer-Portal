from http.client import HTTPResponse
import re
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, make_response, session
from pymongo import MongoClient
from datetime import datetime
import pytz

cluster = MongoClient(
    "mongodb+srv://rahulvk:rvk4551@cluster0.c8dkc.mongodb.net/?retryWrites=true&w=majority")

db = cluster["answer-portal"]
user_collection = db["users"]
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = '123456790'

@app.route('/submit-answer', methods = ['POST','GET'])
def submit():
    if 'email' in session:
        data = request.form
        answer = data["answer"]
        collection = db["answers"]
        a = collection.find_one({"answers":answer})
        if a:
            tz_NY = pytz.timezone('Asia/Kolkata') 
            datetime_NY = datetime.now(tz_NY)
            t = datetime_NY.strftime("%H:%M:%S")
            user_collection.update_one({"email":session['email']}, {"$set": { "answer_status": True, "score":100, "time": t}})
            return "Your Answer is Correct"
        else:
            return render_template("index.html", answer_wrong = True)
    else:
        return redirect(url_for('index'))

@app.route('/', methods=['POST','GET'])
def index():
    if 'email' in session:
        h = user_collection.find_one({"email": session['email']})
        if h:
            return render_template("index.html")
    if request.method == "POST":
        details = request.form
        email = details["email"]
        password = details["password"]
        lg = user_collection.find_one({"email": email})
        if lg:
            if email == lg['email'] and password == lg['password']:
                session['email'] = email
        if 'email' in session:
            if session['email'] == email:
                return render_template("index.html")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect(url_for('index'))


app.secret_key = 'supersecret'

