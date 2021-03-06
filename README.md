## Çatalhöyük

![Example map of the city of Nijmegen](doc/nijmegen.png)

This tool generates an image of a specific part of Google Maps using a custom theme. Themes are defined using the standard [Google API style format](https://developers.google.com/maps/documentation/javascript/style-reference). This can be done textually, but also visually using tools like [Snazzy Maps](https://snazzymaps.com/editor) and [MapStylr](http://www.mapstylr.com).

### Installation

This project crucially depends on `selenium`. For Selenium to interface with your browser, you will need a web driver. This project assumes the Chrome Driver by default. It can be downloaded [directly from the Chromium project](https://sites.google.com/a/chromium.org/chromedriver/downloads), but is also provided as `chromedriver` in some package repositories.

Selenium and all other Python dependencies can be easily installed by calling `pip install -r requirements.txt`.

### Usage and troubleshooting

`catalhoyuk.py` is a command-line utility, running completely headless. In its most basic form, all it requires you to specify is a Google API key and a pair of coordinates. The latter can be easily extracted from a Google Maps URL.

Depending on your use-case, you may want to specify larger dimensions. This should typically also be paired with larger tile dimensions, to avoid long waiting times as catalhoyuk pans across the map.

Furthermore, you may want to specify and/or modify custom themes. Several basic themes have been included in the `themes` directory.

#### Unrendered areas

If you're experiencing unrendered areas in your output image, your coordinates may be too close to the edge of a rendered area in Google Maps. In that case, reduce the tile dimensions so that panning actually crosses a Google Maps area border and all required areas are rendered. Alternatively, depending on your specific case, it may be more efficient to increase image dimensions (and manually crop afterwards) instead of reducing tile dimensions.

#### Command-line interface

```
Usage:
    catalhoyuk.py <Google_API_key> <latitude> <longitude>
        [--zoom=<level>] [--theme=<filename>] [--output=<filename>]
        [--width=<width>] [--height=<height>]
        [--tilewidth=<tilewidth>] [--tileheight=<tileheight>]

Options:
    -h --help                  Show this screen.
    --version                  Show version.
    --zoom=<level>             Zoom level [default: 13]
    --width=<width>            Resulting image width in px [default: 750]
    --height=<height>          Resulting image height px [default: 500]
    --tilewidth=<tilewidth>    Resulting image tilewidth in px [default: 750]
    --tileheight=<tileheight>  Resulting image tileheight in px [default: 500]
    --theme=<filename>         The theme file [default: themes/only-roads-grayscale.json]
    --output=<filename>        The output file [default: output.png]
```