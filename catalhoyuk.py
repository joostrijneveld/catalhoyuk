"""Çatalhöyük.

Usage:
    catalhoyuk.py <Google_API_key> <latitude> <longitude>
        [--zoom=<level>] [--theme=<filename>] [--output=<filename>]
        [--width=<width>] [--height=<height>]
        [--tilewidth=<tilewidth>] [--tileheight=<tileheight>]

Options:
    -h --help                  Show this screen.
    --version                  Show version.
    --zoom=<level>             Zoom level [default: 13]
    --width=<width>            Resulting image width in px [default: 500]
    --height=<height>          Resulting image height px [default: 500]
    --tilewidth=<tilewidth>    Resulting image tilewidth in px [default: 500]
    --tileheight=<tileheight>  Resulting image tileheight in px [default: 500]
    --theme=<filename>         The theme file [default: themes/only-roads-blue.json]
    --output=<filename>        The output file [default: output.png]
"""

import os
import io
import tempfile
import math
from time import sleep

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import jinja2

from docopt import docopt
from schema import Schema, Use

args = docopt(__doc__, version='Çatalhöyük 0.2')

schema = Schema({
    '<latitude>': Use(float, error='Latitude should be a decimal number'),
    '<longitude>': Use(float, error='Latitude should be a decimal number'),
    '--zoom': Use(float, error='Zoom level should be a decimal number'),
    # TODO This should be more strict
    '--theme': Use(str),
    # TODO This should be more strict
    '--output': Use(str),
    '--width': Use(int, error='Width should be an integer'),
    '--height': Use(int, error='Height should be an integer'),
    '--tilewidth': Use(int, error='Tile width should be an integer'),
    '--tileheight': Use(int, error='Tile height should be an integer'),
    '<Google_API_key>': Use(str),
})

args = schema.validate(args)

DRIVER = 'chromedriver'
TEMPLATE_FILE = "template.html.j2"

twidth = args['--tilewidth']
theight = args['--tileheight']

margins = (86, 10, 30, 0)  # top right bottom left


with open(args['--theme'], 'r') as themefile:
    style = themefile.read()

j2loader = jinja2.FileSystemLoader(searchpath="./")
j2env = jinja2.Environment(loader=j2loader)
template = j2env.get_template(TEMPLATE_FILE)
output = template.render(api_key=args['<Google_API_key>'],
                         latitude=args['<latitude>'],
                         longitude=args['<longitude>'],
                         zoom=args['--zoom'],
                         style=style)

tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.html')

tmp.write(output.encode('utf-8'))
tmp.flush()

tmp_path = 'file://' + tmp.name

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")  # prevent offsets
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)
driver.get(tmp_path)
driver.set_window_size(twidth + margins[1] + margins[3], theight + margins[0] + margins[2])

# Let's call the lat/long center the origin.
# We should go half of args[--width] and args[--height to the top-left],
# rounded up to tiles of twidth / theight;
# these tiles can then be stitched and cropped as necessary.
# Note that this is not optimal, but avoids manual px vs coordinate conversions

# for easier computation, keep the middle tile with its center on the origin
# means we approach each half separately
halfwidth = args['--width'] / 2
halfheight = args['--height'] / 2

# guaranteed non-negative when dimensions are non-negative
extra_halfwidth_tiles = math.ceil((halfwidth - twidth / 2) / twidth)
extra_halfheight_tiles = math.ceil((halfheight - theight / 2) / theight)

fullwidth = (2*extra_halfwidth_tiles + 1) * twidth
fullheight = (2*extra_halfheight_tiles + 1) * theight

# first let's create an uncropped image that combines all tiles
output_img = Image.new('RGB', (fullwidth, fullheight))

# TODO this sleep seems to be enough after panning. A nice alternative would be
# to listen to Javascript events, but that's more difficult..
PANSLEEP = 5

# pan to top-left tile
driver.execute_script(f'map.panBy({-extra_halfwidth_tiles * twidth},{-extra_halfheight_tiles * theight})')
print(f"Panning by {-extra_halfwidth_tiles * twidth} {-extra_halfheight_tiles * theight}")
sleep(PANSLEEP)

# plus one for the middle tile
for x in range(2*extra_halfwidth_tiles + 1):
    if x > 0:  # if this is not the first column
        # pan to the top of the next column
        driver.execute_script(f'map.panBy({twidth},{-(fullheight - theight)})')
        print(f'next col: map.panBy({twidth},{-(fullheight - theight)})')
        sleep(PANSLEEP)

    for y in range(2*extra_halfheight_tiles + 1):
        if y > 0:  # if this is not the first row
            # pan to the next row
            driver.execute_script(f'map.panBy(0,{theight})')
            print(f'next row: map.panBy(0,{theight})')
            sleep(PANSLEEP)

        screenshot = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot))
        # crop off the scroll bar and Google logo
        # TODO because of this, the lat / lng is no longer the exact center
        # but it does not really show on a large map
        image = image.crop((0, 0, twidth, theight))

        output_img.paste(image, (x * twidth, y * theight))

# crop off the rounding
hpad = (fullwidth - args['--width']) // 2
vpad = (fullheight - args['--height']) // 2

output_img = output_img.crop((hpad, vpad, args['--width'] + hpad, args['--height'] + vpad))
output_img.save(args['--output'])

driver.quit()
os.remove(tmp.name)
