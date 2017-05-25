import sys
from flask import Flask, render_template, send_from_directory, jsonify

sys.path.append('server')

import yahoo_queries

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/ticker/<ticker>')
def ticker(ticker):
    collection = yahoo_queries.fetch(ticker)
    return jsonify(collection)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


if __name__ == "__main__":
    app.run(debug=True)
