# -*- coding: utf-8 -*-

#   2019/8/6 0006 下午 3:22     

__author__ = 'RollingBear'

import os
import sys
import cv2 as cv
from PIL import Image

import logging
import traceback
from logging.handlers import RotatingFileHandler

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  %(threadName)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    stream=sys.stdout)

Rthandler = RotatingFileHandler('httpIpcHALog.log', maxBytes=10 * 1024 * 1024, backupCount=10)
Rthandler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s  %(threadName)s  %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
Rthandler.setFormatter(formatter)
logger = logging.getLogger('httpIpcHA')
logger.addHandler(Rthandler)


def imageFormatConversion(picPath):
    img = cv.imread(picPath, 0)
    w, h = img.shape[::-1]
    infile = picPath
    outfile = os.path.splitext(infile)[0] + ".jpg"
    img = Image.open(infile)
    img = img.resize((int(w / 2), int(h / 2)), Image.ANTIALIAS)
    try:
        if len(img.split()) == 4:
            # prevent IOError: cannot write mode RGBA as BMP
            r, g, b, a = img.split()
            img = Image.merge("RGB", (r, g, b))
            img.convert('RGB').save(outfile, quality=70)
            os.remove(picPath)
        else:
            img.convert('RGB').save(outfile, quality=70)
            os.remove(picPath)
        return outfile
    except Exception as e:
        logger.error(traceback.format_exc())


if __name__ == '__main__':
    imageFormatConversion(r"C:\Users\lenovo\Desktop\newI\s.png")
