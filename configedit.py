import os
import configparser
from settings import CONFIG_FILE, BASE_DIR

Config = configparser.ConfigParser()


def writeToConf(section, option, value):
    Config.read(CONFIG_FILE)
    Config.set(section, option, value)

    with open(CONFIG_FILE, 'w') as conf_file:
        Config.write(conf_file)


def printDatasets(args=None):
    profile = args[0]
    datasets_dir = os.path.join(BASE_DIR, 'datasets', profile)

    datasets = []
    for f in os.listdir(datasets_dir):
        if f.endswith(".dat"):
            name = f.split(".")[0]
            if name not in datasets:
                datasets.append(name)

    for d in datasets:
        print(d)


def printModels(args=None):
    profile = args[0]
    models_dir = os.path.join(BASE_DIR, 'models', profile)

    models = []
    for m in os.listdir(models_dir):
        models.append(m)

    for m in models:
        print(m)


def printConfig(args=None):
    with open(CONFIG_FILE, 'r') as conf_file:
        print(conf_file.read())


def setPort(args=None):
    port = args[0]
    writeToConf('SerialData', 'port', port)


def setRate(args=None):
    rate = args[0]
    writeToConf('SerialData', 'baud_rate', rate)


def setEpochs(args=None):
    epochs = args[0]
    writeToConf('NeuralNetworkData', 'epochs', epochs)


def setBatchSize(args=None):
    batch_size = args[0]
    writeToConf('NeuralNetworkData', 'batch_size', batch_size)


def setLayerNeurons(args=None):
    layer = args[0]
    n_neurons = args[1]
    writeToConf('NeuralNetworkData', 'hl' + layer + '_neurons', n_neurons)
