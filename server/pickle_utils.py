import cPickle as pickle
import os

DATA_DIR = 'data'

def get_data_filename(filename):
    return os.path.join(os.path.dirname(__file__), '../{}/{}'.format(DATA_DIR, filename))

def get_pickle_or_store(filename, callback):
    file_path = get_data_filename(filename)
    if os.path.exists(file_path):
        print 'found file, retrieving'
        with open(file_path, 'rb') as input_file:
            data = pickle.load(input_file)
    else:
        print 'not found'
        data = callback()
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)
    return data
