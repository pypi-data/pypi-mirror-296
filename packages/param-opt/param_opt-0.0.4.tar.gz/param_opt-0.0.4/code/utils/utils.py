import os
import torch
import joblib
import numpy as np

def create_dir(path, dir_name):
    path = os.path.join(path, dir_name)

    if not os.path.exists(path):
        os.makedirs(path)
        print(f'{path} was created.')

def launch_tensorboard(log_dir):
    os.system('tensorboard --logdir="' + log_dir + '"')
    return

def to_tensor(array):
    return torch.tensor(array, dtype=torch.float32)


def xy_transform(hparam, x, y):
    scaler = joblib.load(hparam['LOG_DIR'] + '/scaler.gz')

    arr = np.append(x, y).reshape(1, -1)
    arr = scaler.transform(arr)
    arr = arr[0]

    x, y = np.hsplit(arr, [hparam['SPLIT_LOC']])
    return x, y


def xy_inverse_transform(hparam, x, y):
    scaler = joblib.load(hparam['LOG_DIR'] + '/scaler.gz')

    arr = np.append(x, y).reshape(1, -1)
    arr = scaler.inverse_transform(arr)
    arr = arr[0]

    x, y = np.hsplit(arr, [hparam['SPLIT_LOC']])
    return x, y