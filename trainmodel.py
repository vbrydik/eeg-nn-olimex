import os
import pickle
import numpy as np
import network

from random import shuffle
from settings import BASE_DIR

datasets_dir = os.path.join(BASE_DIR, 'datasets')
models_dir = os.path.join(BASE_DIR, 'models')


def select_datasets_paths(profile, datasets_len, datasets_names, a):
    # getting all datasets names
    for d in a[3:]:
        datasets_names.append(d)

    # getting path of datasets
    datasets_path = os.path.join(datasets_dir, profile)

    # sorting datasets in dictionary
    datasets_dict = {}
    all_datasets = os.listdir(datasets_path)
    for n in datasets_names:
        datasets_dict[n] = []
        for d in all_datasets:
            if d.split('.')[0] == n:
                datasets_dict[n].append(d)

    # selecting the most recent datasets
    datasets_paths_dict = {}
    for n in datasets_dict:
        cnt = 0
        leng = len(datasets_dict[n])
        datasets_paths_dict[n] = []

        for i in range(leng):
            if cnt >= int(datasets_len):
                break

            file_path = os.path.join(datasets_path, datasets_dict[n][leng-i-1])
            datasets_paths_dict[n].append(file_path)

            cnt += 1

    return datasets_paths_dict


def create_featureset(datasets_paths):
    fs = []

    # Getting number of lablels (classes)
    num_labels = len(datasets_paths)

    print("Creating features and labels dataset from:")

    # Creating dataset of features and labels
    label_cnt = 0
    for n in datasets_paths:
        for i in datasets_paths[n]:
            print(n, "dataset ", i)
            with open(i, 'rb') as df:
                my_data = pickle.load(df)
                for d in my_data:
                    f = d
                    l = np.zeros(num_labels)
                    l[label_cnt] = 1.0

                    l = list(l)
                    fs.append([f, l])
        label_cnt += 1

    # Shuffling and returning dataset
    shuffle(fs)
    return fs


def create_train_and_test_sets(feature_set, test_size=0.1):
    # Testing size was used for tensorflow, not needed for keras
    features = np.array(feature_set)
    # testing_size = int(test_size * len(features))

    train_x = np.array(list(features[:, 0]))  # [: -testing_size]))
    train_y = np.array(list(features[:, 1]))  # [: -testing_size]))

    # Not used for keras
    test_x = 0  # np.array(list(features[:, 0][-testing_size:]))
    test_y = 0  # np.array(list(features[:, 1][-testing_size:]))

    print("Training {} features and labels".format(len(train_x)))

    return train_x, train_y, test_x, test_y


def train(args=None):
    profile = args[0]
    model_name = args[1]
    datasets_len = args[2]
    datasets_names = []

    # Getting recent datasets paths of datasets
    datasets_paths = select_datasets_paths(
                        profile,
                        datasets_len,
                        datasets_names,
                        args)

    # Creating features datasets
    feature_set = create_featureset(datasets_paths)

    # Splitting sets into training and testing sets
    train_x, train_y, test_x, test_y = create_train_and_test_sets(
        feature_set, test_size=0)

    # Training the network
    network.do_train(train_x, train_y, test_x, test_y, model_name, profile)
