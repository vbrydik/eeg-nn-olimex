import os
import numpy as np
import configparser
import serialReader

from tools.config_extract import configExtract
from keras.models import model_from_json
from settings import BASE_DIR, CONFIG_FILE

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
    classes = conf['classes']
    classes = classes.split(' ')

    Config.read(CONFIG_FILE)
    serial_conf = configExtract(Config, 'SerialData')
    serial_port = serial_conf['port']
    serial_rate = serial_conf['baud_rate']
    serial_data_len = int(serial_conf['data_len'])
    serial_packets = int(n_inputs / serial_data_len)

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

    serial = serialReader.SerialReader()
    serial.open(serial_port, serial_rate)

    try:
        print("Press Ctrl+C to stop prediction.")
        while True:
            v, c, serial_data, s = serial.read(serial_packets)
            pred_x = []
            for _d in serial_data:
                for d in _d:
                    d = d / 1023
                    pred_x.append(d)

            pred_x = [pred_x, np.zeros(n_inputs)]
            prediction = loaded_model.predict(pred_x)[0]
            c = prediction.argmax(axis=-1)
            print("\rPrediction: {}".format(classes[c]), end="")
    except KeyboardInterrupt:
        print("\nPrediction stopped.")

    # Testing the prediction
    # TODO: replace with serial data stream!
    # for _ in range(100):
    #     pred_data = np.random.rand(n_inputs).tolist()
    #     pred_x = [pred_data, np.zeros(n_inputs)]
    #     prediction = loaded_model.predict(pred_x)[0]
    #     print(prediction)
