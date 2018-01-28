# coding: utf-8
import hashlib
import json
import os

from librosa.util import find_files     # NOQA


def sha1(obj, length):
    # 20 bytes
    return hashlib.sha1(str(obj)).digest()[:length]


def sha1_file(path, blocksize=2**20):
    s = hashlib.sha1()
    with open(path, 'rb') as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            s.update(buf)
    return s.digest()


def path_to_name(path):
    return os.path.splitext(os.path.basename(path))[0]


class Setting():
    def __init__(self):
        path = os.path.join(os.getcwd(), 'dejavu.settings.json')
        assert os.path.isfile(path)
        settings = json.load(open(path))
        self.__dict__.update(settings)


settings = Setting()
