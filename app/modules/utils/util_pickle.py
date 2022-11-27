# coding: utf-8
import pickle


def serialize(obj, file_name, log=None):
    if log:
        log(f'serializing to {file_name}...')

    # Overwrites any existing file
    with open(file_name, 'wb') as output:
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)


def de_serialize(file_name, log=None):
    if log:
        log(f'de-serializing from {file_name}...')

    with open(file_name, 'rb') as input:
        obj = pickle.load(input)
        return obj
