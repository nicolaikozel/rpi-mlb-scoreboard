from rgbmatrix import FrameCanvas, graphics


def _draw_line(
    canvas: FrameCanvas,
    y_pos: int,
    x1: int,
    x2: int,
    color: graphics.Color,
    endpoints_only: bool = False,
):
    for j in range(x1, x2):
        if endpoints_only and j > x1 and j < x2 - 1:
            continue
        canvas.SetPixel(j, y_pos, color.red, color.green, color.blue)


def draw_square(
    canvas: FrameCanvas,
    x_pos: int,
    y_pos: int,
    size: int,
    color: graphics.Color,
    outline_only=False,
):
    lower_bound = y_pos
    upper_bound = y_pos + size
    for i in range(lower_bound, upper_bound):
        endpoints_only = outline_only and i > lower_bound and i < upper_bound - 1
        _draw_line(
            canvas=canvas,
            y_pos=i,
            x1=x_pos,
            x2=x_pos + size,
            endpoints_only=endpoints_only,
            color=color,
        )


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
