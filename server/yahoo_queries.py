import datetime
import time
import json
from dateutil.relativedelta import relativedelta
import urllib2
import pickle_utils

def generate_query(ticker, shorten_by=0):
    end_dt = datetime.datetime.now()
    delta = relativedelta(months=3) - relativedelta(days=shorten_by)
    begin_dt = end_dt - delta
    begin = int(time.mktime(begin_dt.timetuple()))
    end = int(time.mktime(end_dt.timetuple()))
    return 'https://l1-query.finance.yahoo.com/v8/finance/chart/{}?period2={}&period1={}&interval=5m&indicators=quote&includeTimestamps=true&includePrePost=true&events=div%7Csplit%7Cearn&corsDomain=finance.yahoo.com'.format(
        ticker, end, begin)

def call_until_full_response(ticker, shorten_by=0):
    query = generate_query(ticker, shorten_by)

    res = urllib2.urlopen(query)
    read_res = res.read()
    json_res = json.loads(read_res)

    timestamps = json_res['chart']['result'][0]['timestamp']

    # Sometimes 3 months is too long and returns short results
    # subtract a day until we get full results list
    if len(timestamps) < 3 or shorten_by > 9:
        shorten_by = shorten_by + 1
        return call_until_full_response(ticker, shorten_by)
    else:
        return (json_res, query)

def filter_timestamps(times, timestamps):
    filtered_timestamps = []
    for i, timestamp in enumerate(timestamps):
        time = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')
        if time in times:
            filtered_timestamps.append({
                'timestamp': timestamp,
                'original_index': i
            })
    return filtered_timestamps

def fetch(ticker, filters=['09:30', '10:00']):
    (json_res, query) = pickle_utils.get_pickle_or_store(ticker + '.pickle', lambda: call_until_full_response(ticker, 0))
    # (json_res, query) = call_until_full_response(ticker, 0)

    
    core = json_res['chart']['result'][0]
    quotes = core['indicators']['quote'][0]

    timestamps = core['timestamp']
    closes = quotes['close']
    lows = quotes['low']
    highs = quotes['high']
    opens = quotes['open']
    volumes = quotes['volume']

    return_val = {
        'collection': [],
        'query': query
    }

    filtered_timestamps = filter_timestamps(filters, timestamps)

    for filtered_ts in filtered_timestamps:
        timestamp = filtered_ts['timestamp']
        i = filtered_ts['original_index']
        volume = volumes[i]
        [hour, minute] = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M').split(':')
        if int(hour + minute) > 1600:
            continue
        time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

        return_val['collection'].append({
            'timestamp': timestamp,
            'date': time,
            'low': lows[i],
            'high': highs[i],
            'open': opens[i],
            'close': closes[i],
            'volume': volume
        })

    return return_val

fetch('NFLX')
