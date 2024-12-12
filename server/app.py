from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import pandas as pd
import numpy as np
import joblib
import bcrypt
import jwt
import datetime
import os
from flask_cors import CORS
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string

# global declarations
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    # more to be added 
    return text;

# / route
@app.route("/", methods=["GET"])
def home():
    return "<h1> Welcome to Fake News Detection Portal </h1>"


