import os
import pickle
import time
import datetime
from settings import BASE_DIR
from tools.data_generator import generate_random_train_data

# Path of all datasets
datasets_path = os.path.join(BASE_DIR, 'datasets')


# Generates dataset path with timestamp and index
def generate_dataset_path(data_dir, data_name, i):
    # Getting timestamp string
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts)
    timestamp = timestamp.strftime('%Y%m%d')

    # Getting index string
    i_str = '{:03}'.format(i)
    t_and_i = '.' + timestamp + '.' + i_str

    return os.path.join(data_dir, data_name) + t_and_i + '.dat'


def collect_data(args=None):
    # Getting arguments
    profile = args[0]
    dataset_name = args[1]
    n_samples = int(args[2])

    # Collects data until we have wanted ammount of data
    data = []
    while len(data) != n_samples:
        print("\r> Collecting: {: 5} / {: 5}".format(
            len(data) + 1, n_samples), end="")
        # TODO: replace with serial data collection!
        data.append(generate_random_train_data(1)[0])

    dataset_dir = os.path.join(datasets_path, profile)

    # Creating dataset directory
    if not os.path.exists(dataset_dir):
        os.mkdir(dataset_dir)

    incr = 1
    dataset_path = generate_dataset_path(dataset_dir, dataset_name, incr)
    while os.path.exists(dataset_path):
        incr = incr + 1
        dataset_path = generate_dataset_path(dataset_dir, dataset_name, incr)

    # Writing data to a file
    with open(dataset_path, 'wb') as df:
        pickle.dump(data, df)
        df.close()

    print("\nSaved to: {}".format(dataset_path))
