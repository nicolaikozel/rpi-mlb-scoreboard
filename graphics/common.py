def get_x_pos_for_centered_text(center_pos: int, text: str, font_width: int) -> int:
    return abs(center_pos - ((len(text) * font_width) / 2))


def get_x_pos_for_centered_text_and_obj(center_pos: int, text: str, font_width: int, obj_width: int) -> int:
    return abs(center_pos - ((obj_width + (len(text) * font_width)) / 2))
