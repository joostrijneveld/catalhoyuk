## Çatalhöyük

This tool generates an image of a specific part of Google Maps using a custom theme. Themes are defined using the standard [Google API style format](https://developers.google.com/maps/documentation/javascript/style-reference). This can be done textually, but also visually using tools like [Snazzy Maps](https://snazzymaps.com/editor) and [MapStylr](http://www.mapstylr.com).

### Installation

This project crucially depends on `selenium`. For Selenium to interface with your browser, you will need a web driver. This project assumes the Chrome Driver by default. It can be downloaded [directly from the Chromium project](https://sites.google.com/a/chromium.org/chromedriver/downloads), but is also provided as `chromedriver` in some package repositories.

Selenium and all other Python dependencies can be easily installed by calling `pip install -r requirements.txt`.

### Usage
```
  catalhoyuk.py <Google_API_key> <latitude> <longitude> [--zoom=<level>] [--theme=<filename>] [--width=<width>] [--height=<height>] [--output=<output>]

Options:
  -h --help            Show this screen.
  --version            Show version.
  --zoom=<level>       Zoom level [default: 10]
  --width=<width>      Resulting image width in px [default: 500]
  --height=<height>    Resulting image height px [default: 500]
  --theme=<filename>   The theme file [default: themes/only-roads-blue.json]
  --output=<filename>  The output file [default: output.png]
```