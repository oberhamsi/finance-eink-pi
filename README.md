small python skript to display tradegate data on a waveshare e-ink

important

 * you need locale "de_AT.UTF-8 UTF-8" installed. do so in raspi-config's Localization setting
 * install the only dependency python-pil
 * the code is configured for a 3.7 inch display. every size needs a different library which you have to put into `lib/`. see the waveshare documentation https://github.com/waveshare/e-Paper/tree/master/RaspberryPi_JetsonNano/python
 * for different display sizes change `width` and `height` in main.py.
 * symbols.py holds the stocks to display and optionally the owned lots.

all data is directly pulled from JSON endpoints at tradegate. only for private use.

main.py works in two modes: if the login-user is "pi" it displays on the e-ink display. for any other username it starts in debug mode and outputs a preview image.

hardware used for development

 * waveshare 3.7 inch with HAT https://www.waveshare.com/3.7inch-e-paper-hat.htm
 * rasperry pi zero wh https://www.raspberrypi.org/products/raspberry-pi-zero-w/
