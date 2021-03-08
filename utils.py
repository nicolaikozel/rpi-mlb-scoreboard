import os


def get_abs_file_path(path: str) -> str:
    dir = os.path.dirname(__file__)
    return os.path.join(dir, path)
