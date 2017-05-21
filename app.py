import urllib2
import json
import datetime
from flask import Flask, render_template

def to_timestamp(str_date):
    return int(datetime.datetime.strptime(str_date, '%m/%d/%Y|%H:%M').strftime("%s"))

def generate_query(ticker, begin, end):
    begin = to_timestamp(begin)
    end = to_timestamp(end)
    if begin > end:
        raise ValueError('End date must be greater than begin date')

    return 'https://l1-query.finance.yahoo.com/v8/finance/chart/{}?period2={}&period1={}&interval=5m&indicators=quote&includeTimestamps=true&includePrePost=true&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'.format(
        ticker, end, begin)

def fetch(ticker):
    query = generate_query(ticker, '02/21/2017|9:30', '05/21/2017|16:00')

    res = urllib2.urlopen(query)
    read_res = res.read()
    json_res = json.loads(read_res)

    core = json_res['chart']['result'][0]
    quotes = core['indicators']['quote'][0]

    timestamps = core['timestamp']
    closes = quotes['close']
    volumes = quotes['volume']

    collection = []
    for i, timestamp in enumerate(timestamps):
        volume = volumes[i]
        if volume == 0:
            continue
        time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        collection.append({
            'date': time,
            'close': closes[i],
            'volume': volume
        })

    return collection

app = Flask(__name__)

@app.route('/<ticker>')
def index(ticker):
    collection = fetch(ticker)
    return render_template('table.html', collection=collection)


if __name__ == "__main__":
    app.run(debug=True)


# print json_res['chart']['result'][0]['meta']['currency']