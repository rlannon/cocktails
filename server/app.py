# Cocktails API
# app.py
# Copyright 2020 Riley Lannon

# required imports (flask, etc.)
from flask import  Flask, request, redirect, render_template, url_for, json, jsonify
from flask_cors import CORS, cross_origin
from flaskext.markdown import Markdown
import psycopg2
import os

# initialize the flask app
app = Flask(__name__)

# initialize CORS to allow API access
# todo: uncomment this to enable CORS
# cors = CORS(app, resources={r'/api/*': {"origins": "*"}})

# initialize the markdown rendering library with the tables extension -- this is used for the API's default homepage
Markdown(app, extensions=['tables', 'markdown.extensions.tables'])

# get the database information from our environment
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_PORT = os.environ.get('DATABASE_PORT')

# connect to the database
db = psycopg2.connect(
    DATABASE_URL,
    port=DATABASE_PORT,
    sslmode='require'
)
cur = db.cursor()

# A const string for the API's base url
API_URL_BASE = "/api/v1/"

# index.html
@app.route('/')
def index():
    return render_template('index.html')
