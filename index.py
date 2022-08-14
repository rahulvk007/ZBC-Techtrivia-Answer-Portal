import re
from flask import Flask, render_template, request, redirect, send_from_directory, url_for, make_response

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

