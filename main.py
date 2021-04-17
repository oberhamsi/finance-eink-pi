#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import locale
import time
import urllib.request, json 
from PIL import Image,ImageDraw,ImageFont, ImageOps

from symbols import symbols
IS_RASP = os.environ['LOGNAME'] == 'pi'

if IS_RASP:
    libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)
    from waveshare_epd import epd3in7



locale.setlocale(locale.LC_ALL, 'de_AT.utf8')
ubuntuFont = os.path.join(os.path.dirname(os.path.realpath(__file__)), "UbuntuMono-R.ttf")
font16 = ImageFont.truetype(ubuntuFont, 16)
font18 = ImageFont.truetype(ubuntuFont, 18)

symbols = sorted(symbols, key=lambda k: k['name'])

def nf(val):
    return locale.format_string('%.2f', val)

def toNum(val):
    if (type(val) == str):
        val = val.replace('%', '')
        val = locale.atof(val)
    return val

def nfPlus(val):
    return locale.format_string('%+.2f', val) + '€'

def drawImage(draw, startPoint, isin):
    chartImg = Image.open(urllib.request.urlopen('https://www.tradegate.de/images/charts/tdt/' + isin + '.png'))
    chartImg = chartImg.crop( 
        (0, 0, chartImg.size[0], chartImg.size[1] - 17) 
    )
    chartImg = ImageOps.invert(chartImg.convert('L'))
    chartImg = ImageOps.autocontrast(chartImg, cutoff=8)
    offset = (startPoint[0], startPoint[1] - 20)
    draw.bitmap(offset, chartImg)
    #chartImg.save(isin + '.png')

width=480
height=280
image = Image.new('L', (width, height), 0xFF)
draw = ImageDraw.Draw(image)
y=32
lineHeight=52

cols = [2, 70, 150, 
    260, 340]
colTexts = [
    'Symbol', 
    'Price'.rjust(7), 
    '+/-'.rjust(8), 
    'Low/High'.rjust(6), 
    time.strftime("%H:%M:%S", time.localtime()).rjust(17)
]
for idx, colText in enumerate(colTexts):
    draw.text((cols[idx], 0), colText, font=font16, fill=0)

for symbol in symbols:
    with urllib.request.urlopen("https://www.tradegate.de/refresh.php?isin=" + symbol['isin']) as url:
        data = json.loads(url.read().decode())
        price = toNum(data['last'])
        cost = 0
        worth = 0
        for lot in symbol['lots']:
            cost += lot['shares'] * lot['cost']
            worth += lot['shares'] * price
        dayLow = toNum(data['low'])
        dayHigh = toNum(data['high'])
        delta = toNum(data['delta'])
        vals = [
            symbol['name'],
            nf(price).rjust(6),
            data['delta'].rjust(9),
            nf(dayHigh).rjust(6)
        ]
        lowerVals = [
            None,
            None,
            nfPlus(worth - cost).rjust(9),
            nf(dayLow).rjust(6)
        ]
        for idx, val in enumerate(vals):
            font = font18 if idx < 2 else font16
            offsetY = 0 if idx < 2 else -9
            draw.text((cols[idx], y + offsetY), val, font=font, fill=0)
            lowerVal = lowerVals[idx]
            if lowerVal:
                draw.text((cols[idx], y+20 + offsetY), lowerVal, font=font16, fill=0)
        try:
            drawImage(draw, (cols[-1], y), symbol['isin'])
        except Exception as e:
            print("error drawing for", symbol['code'], e)
    y += lineHeight


if IS_RASP:
    epd = epd3in7.EPD()
    epd.init(0)
    epd.Clear(0xFF, 0)
    epd.display_4Gray(epd.getbuffer_4Gray(image))
    #epd.init(0)
    #epd.Clear(0xFF, 0)
    epd.sleep()
else:
    image.show()

