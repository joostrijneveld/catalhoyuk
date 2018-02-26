"""Çatalhöyük.

Usage:
  catalhoyuk.py <Google_API_key> <latitude> <longitude> [--zoom=<level>] [--theme=<filename>] [--width=<width>] [--height=<height>] [--output=<output>]

Options:
  -h --help            Show this screen.
  --version            Show version.
  --zoom=<level>       Zoom level [default: 10]
  --width=<width>      Resulting image width in px [default: 500]
  --height=<height>    Resulting image height px [default: 500]
  --theme=<filename>   The theme file [default: themes/only-roads-blue.json]
  --output=<filename>  The output file [default: output.png]
"""

import os
import io
import tempfile
# from time import sleep

from PIL import Image
from selenium import webdriver
import jinja2

from docopt import docopt
from schema import Schema, Use

args = docopt(__doc__, version='Çatalhöyük 0.1')

schema = Schema({
    '<latitude>': Use(float, error='Latitude should be a decimal number'),
    '<longitude>': Use(float, error='Latitude should be a decimal number'),
    '--zoom': Use(float, error='Zoom level should be a decimal number'),
    # TODO This should be more strict
    '--theme': Use(str),
    # TODO This should be more strict
    '--output': Use(str),
    '--width': Use(int, error='Width should be an integer'),
    '--height': Use(int, error='Width should be an integer'),
    '<Google_API_key>': Use(str),
})
args = schema.validate(args)

DRIVER = 'chromedriver'
TEMPLATE_FILE = "template.html.j2"

# This appears to give us the right size of tiles in Chromium
# TODO figure this out dynamically
browserwidth = args['--width'] + 10  # 10 for Chromium
browserheight = args['--height'] + 125 + 25  # 125 for Chromium, 25 for logo

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

tmp = tempfile.NamedTemporaryFile(delete=False)

tmp.write(output.encode('utf-8'))
tmp.flush()

tmp_path = 'file://' + tmp.name

driver = webdriver.Chrome(DRIVER)
driver.get(tmp_path)
driver.set_window_size(browserwidth, browserheight)

# TODO pan to different locations around this tile
# driver.execute_script('map.panTo(new google.maps.LatLng(..., ...));')

# TODO this seems to be enough after panning. A nicer alternative would be to
#   listen to Javascript events, but that's more difficult
# sleep(.5)

screenshot = driver.get_screenshot_as_png()
image = Image.open(io.BytesIO(screenshot))
image = image.crop((0, 0, args['--width'], args['--height']))
image.save(args['--output'])

driver.quit()
os.remove(tmp.name)
