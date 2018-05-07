import os
import numpy as np
import configparser

from tools.config_extract import configExtract
from keras.models import model_from_json
from settings import BASE_DIR

Config = configparser.ConfigParser()


def predict(args):
    profile = args[0]
    model_name = args[1]

    # Getting files paths
    models_path = os.path.join(BASE_DIR, 'models', profile, model_name)
    json_path = os.path.join(models_path, model_name + '.json')
    weights_path = os.path.join(models_path, model_name + '.h5')
    conf_path = os.path.join(models_path, model_name + '.ini')

    # Reading data from model config file
    Config.read(conf_path)
    conf = configExtract(Config, 'NetworkData')
    n_inputs = int(conf['inputs'])
    # n_outputs = int(conf['outputs'])

    # Reading from json path
    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)

    # Loading weights from file to model
    loaded_model.load_weights(weights_path)
    print("Model loaded from disk!")

    # Compiling the model
    loaded_model.compile(
        loss="binary_crossentropy", optimizer='rmsprop', metrics=['accuracy'])

    # Testing the prediction
    # TODO: replace with serial data stream!
    pred_x = [[0.2, 0.5, 0.4, 0.8, 0.8, 0.4], np.zeros(n_inputs)]
    prediction = loaded_model.predict(pred_x)[0]
    print(prediction)
