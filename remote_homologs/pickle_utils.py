import os
import pickle


def save(data, path):
    with open(path, "wb") as f:
        pickle.dump(data, f)


def check_b4_save(data, path):
    if not os.path.exists(path):
        save(data, path)


def load(path):
    with open(path, "rb") as f:
        return pickle.load(f)
