from __future__ import division
import datetime

def map_collection_item(timestamp, i, quotes):
    return {
        'timestamp': timestamp,
        'date': datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        'low': quotes['low'][i],
        'high': quotes['high'][i],
        'open': quotes['open'][i],
        'close': quotes['close'][i],
        'volume': quotes['volume'][i]
    }

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

def filter_days_start_ends(timestamps, quotes, s1, e1, s2, e2):
    filtered = {}
    for i, timestamp in enumerate(timestamps):
        time = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M')
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        if date not in filtered:
          filtered[date] = {}
        if time in [s1, e1, s2, e2]:
            if time == s1:
              filtered[date][s1] = map_collection_item(timestamp, i, quotes)
            if time == e1:
              filtered[date][e1] = map_collection_item(timestamp, i, quotes)
            if time == s2:
              filtered[date][s2] = map_collection_item(timestamp, i, quotes)
            if time == e2:
              filtered[date][e2] = map_collection_item(timestamp, i, quotes)

              s1_close = filtered[date][s1]['close']
              e1_close = filtered[date][e1]['close']
              change_1 = abs(s1_close - e1_close)
              direction_1 = 'up' if e1_close > s1_close else 'down'
              filtered[date]['1_direction'] = direction_1
              filtered[date]['1_percentage_change'] = change_1 / s1_close * 100
              s2_close = filtered[date][s2]['close']
              e2_close = filtered[date][e2]['close']
              change_2 = abs(s2_close - e2_close)
              direction_2 = 'up' if e2_close > s2_close else 'down'
              filtered[date]['2_direction'] = direction_2
              filtered[date]['2_percentage_change'] = change_2 / s2_close * 100
              continue
    return filtered


def get_all(quotes, timestamps):
    collection = []
    for i, timestamp in enumerate(timestamps):
        [hour, minute] = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M').split(':')
        if int(hour + minute) > 1600 or int(hour + minute) < 930:
            continue
        collection.append(map_collection_item(timestamp, i, quotes))
    return collection


def get_filtered(quotes, timestamps, times = ['10:00', '10:30']):
    filtered_timestamps = filter_timestamps(times, timestamps)
    collection = []
    for el in filtered_timestamps:
        [hour, minute] = datetime.datetime.fromtimestamp(el['timestamp']).strftime('%H:%M').split(':')
        if int(hour + minute) > 1600 or int(hour + minute) < 930:
            continue
        collection.append(map_collection_item(el['timestamp'], el['original_index'], quotes))
    return collection

def calculate_probabilities(quotes, timestamps, s1, e1, s2, e2):
    return filter_days_start_ends(timestamps, quotes, s1, e1, s2, e2)

