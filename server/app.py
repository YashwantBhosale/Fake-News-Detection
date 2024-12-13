from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from bson import ObjectId
import numpy as np
import joblib
# import bcrypt
# import jwt
# import datetime
import os
from flask_cors import CORS
import re
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string
from dotenv import load_dotenv

# global declarations
ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

load_dotenv()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\[.*?]", "", text)
    url = re.compile(r"https?://\S+|www.\.\S+")
    text = url.sub(r"", text)
    text = re.sub(r"<.*?>", "", text)
    text = re.sub(r"[%s]" % re.escape(string.punctuation), "", text)
    text = re.sub(r"\w*\d\w*", "", text)
    return text


def stem_text(text):
    text = [ps.stem(word) for word in text.split() if word not in stop_words]
    return " ".join(text)


"""
SECRET_KEY = os.getenv("SECRET_KEY")
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI) # db client
"""

# load pre-fitted vectorizer
vectorizer = joblib.load("vectorizer.pkl")

app = Flask(__name__)
CORS(app)

# load pre-trained model
model = joblib.load("model.pkl")


# / route
@app.route("/", methods=["GET"])
def home():
    return "<h1> Welcome to Fake News Detection Portal </h1>"


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        # Ensure that 'news' exists in the incoming data
        if "news" not in data:
            return jsonify({"error": "News field missing!"}), 401

        # Following is jwt code uncomment if user authentication is being used
        """
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({ "error": "JWT token missing!" }), 401
        """

        # Following code is for storing news in database again use if authentication + database is being used
        """
        db = client["news"]
        collection = db["news"]
        users_collection = db["users"]
        """

        """
        try:
            decoded_token = jwt.decode(
                token.split(" ")[1], SECRET_KEY, algorithms=["HS256"]
            )
            user = users_collection.find_one(
                {"_id": ObjectId(decoded_token["user_id"])}
            )
            if not user:
                return jsonify({"error": "User not found"}), 404
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401 
        """

        # clean and preprocess the text
        raw_text = data["news"]
        cleaned_text = clean_text(raw_text)
        stemmed_text = stem_text(cleaned_text)

        vectorized_data = vectorizer.transform([stemmed_text])
        prediction = model.predict(vectorized_data)
        # prediction = prediction[0]

        """
        _news = {
            "user_id": str(user["_id"]),
            "text": raw_text,
            "preprocessor_text": stemmed_text,
            "prediction": prediction,
            "createdAt": datetime.datetime.now().isoformat()
        }

        collection.insert_one(_news)
        """

        final_prediction = "Real" if prediction == 1 else "Fake"
        return jsonify({"prediction": str(final_prediction)}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


"""
    Authentication is usually irrelevant for such applications where user just wants to check if
    given news is fake or not. But i have still included the authentication code just in
    case i find some better use case and need it. It also includes jwt based authentication.
"""

"""
@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json(force=True)
        db = client["news"]
        collection = db["users"]

        user = collection.find_one({"email" : data["email"]})

        if user:
            return jsonify({"error" : "User already exists!"}), 400

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(data["password"].encode("utf-8"), salt)
        
        user = {
            "username" : data["username"],
            "password" : hashed_password,
            "email" : data["email"],
            "role" : "user",
            "created_at" : datetime.datetime.now().isoformat() # store data in iso format
        }

        collection.insert_one(user)

        # Pending: create jwt here and directly sign the user in
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        db = client["news"]
        collection = db["users"]

        user = collection.find_one({"email" : data["email"]})

        if user is None:
            return jsonify({ "error" : "User not Found!" }), 404

        hashed_password = user["password"]

        if bcrypt.checkpw(data["password"].encode("utf-8"), hashed_password):
            # generate jwt token
            payload = {
                "user_id" : str(user["_id"]),
                "role" : user["role"],
                "exp" : datetime.datetime.uctnow() + datetime.timedelta(hours=1) # 1 hour expiration time
            }

            token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

            return (
                jsonify(
                    {
                        "message" : "Login successful!",
                        "user" : {
                            "username" : user["username"],
                            "email" : user["email"],
                            "role" : user["role"],
                        },
                        "token" : token
                    }
                ), 200
            )
        else:
            return jsonify({"error": "Invalid Password!"}), 401
    except Exception as e:
        return jsonify({ "error": str(e) }), 500
        

"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
