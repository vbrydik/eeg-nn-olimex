import os

import trainmodel
import collectdata
import predict
import configedit

from settings import BASE_DIR

help_file = os.path.join(BASE_DIR, 'help.txt')


def clear_scr(args):
    os.system('cls')


def help_print(args=None):
    with open(help_file, 'r') as f:
        print(f.read())


COMMANDS = {
    # main functions
    'collectdata':    'collectdata.collect_data',
    'train':          'trainmodel.train',
    'predict':        'predict.predict',
    # helper functions
    'help':           'help_print',
    'cls':            'clear_scr',
    # print functions
    'print_config':   'configedit.printConfig',
    'print_datasets': 'configedit.printDatasets',
    'print_models':   'configedit.printModels',
    # config functions
    'set_port':       'configedit.setPort',
    'set_rate':       'configedit.setRate',
    'set_epochs':     'configedit.setEpochs',
    'set_layer':      'configedit.setLayerNeurons',
    'set_batchsize':  'configedit.setBatchSize',
}


def execute_from_args(args):
    a = args[0]
    if a in COMMANDS:
        eval(str(COMMANDS[a]) + '(' + str(args[1:]) + ')')
