import json
import os

from utils import get_abs_file_path


class Config:
    _conf = {}

    @classmethod
    def _load(cls):
        path = get_abs_file_path(path="config.json")
        cls._conf = json.load(open(path))

    @classmethod
    def get(cls) -> dict:
        if not cls._conf:
            cls._load()
        return cls._conf
