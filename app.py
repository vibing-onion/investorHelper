import sys
import os

dir = [
    'functions',
]

for d in dir:
    # print(os.getcwd() + '/' + d)
    sys.path.insert(0, os.getcwd() + d)

from flask import Flask, jsonify
from functions.api import initialize, search_cik

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Home Page</h1>"

@app.route("/search_cik/<ticker>")
def searchCIK(ticker):
    
    return jsonify(search_cik(ticker))

if __name__ == '__main__':
    initialize()
    app.run(debug=True, use_reloader=False)