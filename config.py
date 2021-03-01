import json
import os

from utils import get_abs_file_path

CONFIG = {}


def load_config():
    path = get_abs_file_path(path="config.json")
    CONFIG = json.load(open(path))