import os


def get_abs_file_path(path):
  dir = os.path.dirname(__file__)
  return os.path.join(dir, path)


def center_text_position(text, center_pos, font_width):
    return abs(center_pos - ((len(text) * font_width) / 2))