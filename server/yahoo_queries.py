from __future__ import division
import datetime
import time
import json
from dateutil.relativedelta import relativedelta
import urllib2
import pickle_utils
import movement_utils
import time

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
    start = time.time()
    (json_res, query) = pickle_utils.get_pickle_or_store(ticker + '.pickle', lambda: call_until_full_response(ticker, 0))
    end = time.time()
    print 'pickle {}'.format(end - start)
    
    core_result = json_res['chart']['result'][0]
    quotes = core_result['indicators']['quote'][0]
    timestamps = core_result['timestamp']

    try:
        start = time.time()
        results = movement_utils.calculate_probabilities(quotes, timestamps, s1, e1, s2, e2)
        end = time.time()
        print 'calc {}'.format(end - start)
    except:
        print '{} errored'.format(ticker)
        return

    total = len(results)
    matches = 0
    for date in results:
        if results[date]['1_direction'] == results[date]['2_direction']:
            matches += 1
    
    percentMatch = matches / total * 100
    print 'ticker: {}, percentMatch: {}, total: {}, matches: {}'.format(ticker, percentMatch, total, matches)

stocks = [
  "AAL",
  "AAPL",
  "ADBE",
  "ADI",
  "ADP",
  "ADSK",
  "AKAM",
  "ALXN",
  "AMAT",
  "AMGN",
  "AMZN",
  "ATVI",
  "AVGO",
  "BIDU",
  "BIIB",
  "BMRN",
  "CA",
  "CELG",
  "CERN",
  "CHKP",
  "CHTR",
  "CTRP",
  "CTAS",
  "CSCO",
  "CTXS",
  "CMCSA",
  "COST",
  "CSX",
  "CTSH",
  "DISCA",
  "DISCK",
  "DISH",
  "DLTR",
  "EA",
  "EBAY",
  "ESRX",
  "EXPE",
  "FAST",
  "FB",
  "FISV",
  "FOX",
  "FOXA",
  "GILD",
  "GOOG",
  "GOOGL",
  "HAS",
  "HSIC",
  "HOLX",
  "ILMN",
  "INCY",
  "INTC",
  "INTU",
  "ISRG",
  "JBHT",
  "JD",
  "KLAC",
  "KHC",
  "LBTYA",
  "LBTYK",
  "LILA",
  "LILAK",
  "LRCX",
  "QVCA",
  "LVNTA",
  "MAR",
  "MAT",
  "MCHP",
  "MDLZ",
  "MNST",
  "MSFT",
  "MU",
  "MXIM",
  "MYL",
  "NCLH",
  "NFLX",
  "NTES",
  "NVDA",
  "ORLY",
  "PAYX",
  "PCAR",
  "PCLN",
  "PYPL",
  "QCOM",
  "REGN",
  "ROST",
  "SBAC",
  "STX",
  "SHPG",
  "SIRI",
  "SWKS",
  "SBUX",
  "SYMC",
  "TMUS",
  "TRIP",
  "TSCO",
  "TSLA",
  "TXN",
  "ULTA",
  "VIAB",
  "VOD",
  "VRSK",
  "VRTX",
  "WBA",
  "WDC",
  "XLNX",
  "XRAY",
  "YHOO"
]

for stock in stocks:
    calc(stock, '09:30', '09:50', '09:50', '10:00')

