import sys
import os

dir = [
    'functions',
]
[sys.path.insert(0, os.getcwd() + d) for d in dir]

from flask import Flask, jsonify
from flask_cors import CORS
from functions.api import sample_data_api

# Create Flask app
app = Flask(__name__)
CORS(app)

# API endpoint
@app.route('/api/v1/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'})

@app.route("/api/v1/sampleData", methods=["GET"])
def home():
    return jsonify(sample_data_api())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)