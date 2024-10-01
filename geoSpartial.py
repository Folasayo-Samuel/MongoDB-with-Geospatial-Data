from flask import Flask, jsonify, make_response
from pymongo import MongoClient
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["geo_database"]
collection = db["places"]

# Endpoint to retrieve all places from the database
@app.route('/place', methods=['GET'])
def get_places():
    places = collection.find({})
    output = []
    for place in places:
        output.append({
            'name':place['name'],
            'location': place['location']
        })
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True, port=5000)