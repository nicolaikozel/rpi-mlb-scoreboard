import argparse
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from views.main_view import MainView


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. (Default: 16)", default=16, type=int)
  parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=32, type=int)
  parser.add_argument("--led-brightness", action="store", help="Sets brightness level. Range: 1..100. (Default: 100)", default=100, type=int)
  parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 = Progressive, 1 = Interlaced. (Default: 1)", default=1, choices=range(2), type=int)
  parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel.")
  parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. (Default: 2)", default=2, choices=range(5), type=int)
  return parser.parse_args()


def create_rgb_matrix_options(args):
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
try:
    print("Press CTRL-C to stop running.")
    MainView(rgb_matrix=rgb_matrix).render()
except KeyboardInterrupt:
    print("\nExiting.\n")
    sys.exit(0)

