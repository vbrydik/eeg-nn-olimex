import os
import numpy as np
import configparser

from tools.config_extract import configExtract
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import Callback

from settings import CONFIG_FILE
from settings import BASE_DIR

np.random.seed(7)

Config = configparser.ConfigParser()


class NNHistory(Callback):
    def __init__(self, e):
        self.epochs = e
        pass

    def on_train_begin(self, logs={}):
        # Training started
        # self.losses = []
        # self.accuracy = []
        pass

    def on_epoch_end(self, epoch, logs={}):
        # self.losses.append(logs.get('loss'))
        # self.accuracy.append(logs.get('acc'))
        print("\r> Epoch: {: 5} / {: 5}   Accuracy: {:2}%".format(
            epoch + 1, self.epochs, logs.get('acc') * 100), end="")

    def on_train_end(self, logs={}):
        # Training ended
        print()
        pass


def do_train(train_x, train_y, test_x, test_y, model_name, profile, classes):
    num_inputs = len(train_x[0])
    num_outputs = len(train_y[0])

    Config.read(CONFIG_FILE)
    config = configExtract(Config, 'NeuralNetworkData')
    Config.clear()

    batch_size = int(config['batch_size'])
    epochs = int(config['epochs'])

    hl1_neurons = int(config['hl1_neurons'])
    hl2_neurons = int(config['hl2_neurons'])

    # Creating a model
    model = Sequential()

    # Adding layers to model
    model.add(Dense(hl1_neurons, input_dim=num_inputs, activation='relu'))
    model.add(Dense(hl2_neurons, activation='relu'))
    model.add(Dense(num_outputs, activation='sigmoid'))

    # Compiling model
    model.compile(
        loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Training callbacks
    history = NNHistory(100)

    # Training model
    model.fit(
        train_x, train_y, epochs=epochs,
        batch_size=batch_size, verbose=0,
        callbacks=[history])

    # Evaluating scores of a model
    scores = model.evaluate(train_x, train_y)
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

    # Getting models path
    models_path = os.path.join(BASE_DIR, 'models')
    profile_path = os.path.join(models_path, profile)
    model_path = os.path.join(profile_path, model_name)
    json_path = os.path.join(model_path, model_name + '.json')
    weights_path = os.path.join(model_path, model_name + '.h5')
    conf_path = os.path.join(model_path, model_name + '.ini')
    print(json_path)
    print(weights_path)

    if not os.path.exists(models_path):
        os.mkdir(models_path)
    if not os.path.exists(profile_path):
        os.mkdir(profile_path)
    if not os.path.exists(model_path):
        os.mkdir(model_path)

    # Writing model to json file
    model_json = model.to_json()
    json_file = open(json_path, 'w')
    json_file.write(model_json)
    json_file.close()

    # Writing some config data about model
    conf_file = open(conf_path, 'w')
    if not Config.has_section('NetworkData'):
        Config.add_section('NetworkData')
    Config.set('NetworkData', 'inputs', str(num_inputs))
    Config.set('NetworkData', 'outputs', str(num_outputs))
    Config.set('NetworkData', 'classes', classes)
    Config.write(conf_file)
    conf_file.close()

    # Save weights of the model
    model.save_weights(weights_path)
    print("Model saved to disk!")
