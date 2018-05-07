import os

from trainmodel import train
from collectdata import collect_data
from predict import predict
from settings import BASE_DIR

help_file = os.path.join(BASE_DIR, 'help.txt')


def clear_scr(args):
    os.system('cls')


def help_print(args=None):
    with open(help_file, 'r') as f:
        print(f.read())


COMMANDS = {
    'collectdata':  'collect_data',
    'train':        'train',
    'predict':      'predict',
    'help':         'help_print',
    'cls':          'clear_scr',
}


def execute_from_args(args):
    a = args[0]
    if a in COMMANDS:
        eval(str(COMMANDS[a]) + '(' + str(args[1:]) + ')')
