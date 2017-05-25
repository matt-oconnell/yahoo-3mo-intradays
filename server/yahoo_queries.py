import datetime
import time
import json
from dateutil.relativedelta import relativedelta
import urllib2

def generate_query(ticker):
    now = datetime.datetime.now()
    delta = relativedelta(months=3)
    then = now - delta
    begin = int(time.mktime(then.timetuple()))
    end = int(time.mktime(now.timetuple()))
    return 'https://l1-query.finance.yahoo.com/v8/finance/chart/{}?period2={}&period1={}&interval=5m&indicators=quote&includeTimestamps=true&includePrePost=true&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'.format(
        ticker, end, begin)

def fetch(ticker):
    query = generate_query(ticker)

    res = urllib2.urlopen(query)
    read_res = res.read()
    json_res = json.loads(read_res)

    core = json_res['chart']['result'][0]
    quotes = core['indicators']['quote'][0]

    timestamps = core['timestamp']
    closes = quotes['close']
    volumes = quotes['volume']

    return_val = {
        'collection': [],
        'query': query
    }
    for i, timestamp in enumerate(timestamps):
        volume = volumes[i]
        [hour, minute] = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M').split(':')
        if int(hour + minute) > 1600:
            continue
        time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return_val['collection'].append({
            'timestamp': timestamp,
            'date': time,
            'close': closes[i],
            'volume': volume
        })

    return return_val

fetch('AAPL')