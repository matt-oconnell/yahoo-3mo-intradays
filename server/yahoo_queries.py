from __future__ import division
import datetime
import time
import json
from dateutil.relativedelta import relativedelta
import urllib2
import pickle_utils
import movement_utils
import time
#
import seed_nasdaq100
import seed_custom
import seed_iq_100
import seed_s_p_500

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

    try:
        res = urllib2.urlopen(query)
        read_res = res.read()
        json_res = json.loads(read_res)
    except:
        print '{} errored'.format(ticker)
        return 0

    timestamps = json_res['chart']['result'][0]['timestamp']

    # Sometimes 3 months is too long and returns short results
    # recursively subtract a day until we get full results list
    if len(timestamps) < 3 or shorten_by > 9:
        shorten_by = shorten_by + 1
        return call_until_full_response(ticker, shorten_by)
    else:
        return (json_res, query)

def fetch(ticker):
    (json_res, query) = pickle_utils.get_pickle_or_store(ticker + '.pickle', lambda: call_until_full_response(ticker, 0))

    core_result = json_res['chart']['result'][0]
    quotes = core_result['indicators']['quote'][0]
    timestamps = core_result['timestamp']

    return_val = {
        'collection': [],
        'query': query
    }

    return_val['collection'] = movement_utils.get_filtered(quotes, timestamps)
    return return_val


def calc(ticker, s1, e1, s2, e2):
    try:
        (json_res, query) = pickle_utils.get_pickle_or_store(ticker + '.pickle', lambda: call_until_full_response(ticker, 0))
        core_result = json_res['chart']['result'][0]
        quotes = core_result['indicators']['quote'][0]
        timestamps = core_result['timestamp']
        results = movement_utils.calculate_probabilities(quotes, timestamps, s1, e1, s2, e2)

        total = len(results)
        matches = 0
        for date in results:
            if results[date]['1_direction'] == results[date]['2_direction']:
                matches += 1

    except:
        print '{} errored'.format(ticker)
        return 50
    
    percent_match = matches / total * 100
    print 'ticker: {}, percent_match: {}, total: {}, matches: {}'.format(ticker, percent_match, total, matches)
    return percent_match



# TESTING

seed_stocks = seed_nasdaq100.stocks + seed_custom.stocks + seed_iq_100.stocks + seed_s_p_500.stocks
seed_stocks = list(set(seed_stocks))

def backtest(s1, e1, s2, e2):
    percent_matches = []
    highest = { 'percent': 0, 'ticker': '' }
    lowest = { 'percent': 100, 'ticker': '' }
    for stock in seed_stocks:
        percent_match = calc(stock, s1, e1, s2, e2)
        percent_matches.append(percent_match)
        if percent_match > highest['percent']:
            highest['percent'] = percent_match
            highest['ticker'] = stock
        if percent_match < lowest['percent']:
            lowest['percent'] = percent_match
            lowest['ticker'] = stock

    result_str = '{}, {}, {}, {}\n'.format(s1, e1, s2, e2)
    result_str += 'total percent match average: {}\n'.format(sum(percent_matches) / float(len(percent_matches)))
    result_str += 'highest: {}, at {}\n'.format(highest['ticker'], highest['percent'])
    result_str += 'lowest: {}, at {}\n==========\n'.format(lowest['ticker'], lowest['percent'])
    print result_str

    f = open('results.txt', 'a')
    f.write(result_str)
    f.close()


e1s_and_s2s = ['10:30', '10:30', '10:30', '10:30', '10:30', '10:30', '11:00', '11:00', '11:00', '11:00']
e2s         = ['10:40', '10:50', '11:00', '11:10', '11:20', '11:30', '11:15', '11:20', '11:25', '11:30']

for i in range(len(e2s)):
    backtest('09:30', e1s_and_s2s[i], e1s_and_s2s[i], e2s[i])


