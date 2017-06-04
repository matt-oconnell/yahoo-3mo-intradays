import sys
from flask import Flask, render_template, send_from_directory, jsonify, request

sys.path.append('server')

import yahoo_queries

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/ticker/<ticker>')
def ticker(ticker):
    collection = yahoo_queries.fetch(ticker)
    print collection
    return jsonify(collection)

@app.route('/movement/')
def movement():
    ticker = request.args.get('ticker')
    s1 = request.args.get('s1')
    e1 = request.args.get('e1')
    s2 = request.args.get('s2')
    e2 = request.args.get('e2')
    collection = yahoo_queries.fetch(ticker)
    return jsonify(collection)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('dist', path)


if __name__ == "__main__":
    app.run(debug=True)
