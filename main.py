import argparse
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--led-rows",
        action="store",
        help="Display rows. 16 for 16x32, 32 for 32x32. (Default: 16)",
        default=16,
        type=int,
    )
    parser.add_argument(
        "--led-cols",
        action="store",
        help="Panel columns. Typically 32 or 64. (Default: 32)",
        default=32,
        type=int,
    )
    parser.add_argument(
        "--led-brightness",
        action="store",
        help="Sets brightness level. Range: 1..100. (Default: 100)",
        default=100,
        type=int,
    )
    parser.add_argument(
        "--led-scan-mode",
        action="store",
        help="Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)",
        default=1,
        choices=range(2),
        type=int,
    )
    parser.add_argument(
        "--led-show-refresh",
        action="store_true",
        help="Shows the current refresh rate of the LED panel.",
    )
    parser.add_argument(
        "--led-slowdown-gpio",
        action="store",
        help="Slow down writing to GPIO. Range: 0..4. (Default: 2)",
        default=2,
        choices=range(5),
        type=int,
    )
    return parser.parse_args()


def create_rgb_matrix_options(args: object) -> RGBMatrixOptions:
    options = RGBMatrixOptions()
    options.rows = args.led_rows
    options.cols = args.led_cols
    options.brightness = args.led_brightness
    if args.led_show_refresh:
        options.show_refresh_rate = 1
    if args.led_slowdown_gpio != None:
        options.gpio_slowdown = args.led_slowdown_gpio
    return options


# Parse arguments and initialize the RGB matrix
args = parse_args()
rgb_matrix_options = create_rgb_matrix_options(args=args)
rgb_matrix = RGBMatrix(options=rgb_matrix_options)

# Log
print(f"Running rpi-mlb-scoreboard-({rgb_matrix.height}x{rgb_matrix.width})")

# Render the main view - CTRL-C to exit
### TEMP
from views.base_views import RestartableView
from controllers.looping_views import LoopingViewsController
from views.clock import ClockView

clock_loop_controller = LoopingViewsController(
    views=[
        RestartableView(view=ClockView, rgb_matrix=rgb_matrix, loc="Tor"),
        RestartableView(view=ClockView, rgb_matrix=rgb_matrix, loc="Ist"),
    ],
    view_change_delay=3,
)
clock_loop_controller.start()
#######
try:
    print("Press CTRL-C to stop running.")
    clock_loop_controller.join()
except KeyboardInterrupt:
    print("\nExiting.\n")
    clock_loop_controller.stop()
    clock_loop_controller.join()
    sys.exit(0)
