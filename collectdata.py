import os
import pickle
import time
import datetime
import configparser
import serialReader

from settings import BASE_DIR, CONFIG_FILE
from tools.config_extract import configExtract

datasets_path = os.path.join(BASE_DIR, 'datasets')
Config = configparser.ConfigParser()


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

    Config.read(CONFIG_FILE)
    nn_conf = configExtract(Config, 'NeuralNetworkData')
    n_inputs = int(nn_conf['inputs'])

    serial_conf = configExtract(Config, 'SerialData')
    serial_port = serial_conf['port']
    serial_rate = serial_conf['baud_rate']
    serial_data_len = int(serial_conf['data_len'])
    serial_packets = int(n_inputs / serial_data_len)

    serial = serialReader.SerialReader()
    serial.open(serial_port, serial_rate)

    # Collects data until we have wanted ammount of data
    data = []
    while len(data) != n_samples:
        print("\r> Collecting: {: 5} / {: 5}".format(
            len(data) + 1, n_samples), end="")

        v, c, serial_data, s = serial.read(serial_packets)
        append_data = []

        for _d in serial_data:
            for d in _d:
                d = d / 1023
                append_data.append(d)

        data.append(append_data)

    serial.close()

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
