from rgbmatrix import FrameCanvas, graphics


def draw_diamond(canvas: FrameCanvas, x_pos:int , y_pos:int , size:int, color: graphics.Color):
    x = x_pos
    
    # Top part + middle
    y = y_pos
    for i in range(int(size/2+1)):
        for j in range(x-i, x+i+1):
            canvas.SetPixel(j, y, color.red, color.green, color.blue)
        y += 1
    
    # Bottom part
    y = y_pos + size - 1
    for i in range(int((size-1)/2)):
        for j in range(x-i, x+i+1):
            canvas.SetPixel(j, y, color.red, color.green, color.blue)
        y -= 1

    
