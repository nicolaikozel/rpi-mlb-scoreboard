def center_text(center_pos: int, text: str, font_width: int) -> int:
    return abs(center_pos - ((len(text) * font_width) / 2))


def center_object(center_pos: int, obj_length: int) -> int:
    return abs(center_pos - (obj_length / 2))
