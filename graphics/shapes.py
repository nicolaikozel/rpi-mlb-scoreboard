from rgbmatrix import FrameCanvas, graphics


def _draw_line(
    canvas: FrameCanvas,
    y_pos: int,
    x1: int,
    x2: int,
    endpoints_only: bool,
    color: graphics.Color,
):
    for j in range(x1, x2):
        if endpoints_only and j > x1 and j < x2 - 1:
            continue
        canvas.SetPixel(j, y_pos, color.red, color.green, color.blue)


def draw_diamond(
    canvas: FrameCanvas,
    x_pos: int,
    y_pos: int,
    size: int,
    color: graphics.Color,
    outline_only=False,
):
    if size % 2 == 0:
        raise ValueError("Size must be an odd number.")

    x = x_pos

    # Top part + middle
    y = y_pos
    for i in range(int(size / 2 + 1)):
        _draw_line(
            canvas=canvas,
            y_pos=y,
            x1=x - i,
            x2=x + i + 1,
            endpoints_only=outline_only,
            color=color,
        )
        y += 1

    # Bottom part
    y = y_pos + size - 1
    for i in range(int((size - 1) / 2)):
        _draw_line(
            canvas=canvas,
            y_pos=y,
            x1=x - i,
            x2=x + i + 1,
            endpoints_only=outline_only,
            color=color,
        )
        y -= 1
