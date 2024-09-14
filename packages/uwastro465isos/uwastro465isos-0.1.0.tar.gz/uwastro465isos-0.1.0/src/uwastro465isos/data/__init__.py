import os

def get_data_path(fn):
    _file = os.path.abspath(__file__)
    _dir, _ = os.path.split(_file)
    full_file = os.path.join(_dir, fn)
    return full_file
