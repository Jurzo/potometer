#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

from PIL import Image,ImageDraw,ImageFont

class ImageCreator:

    def __init__(self):
        self.width = 640
        self.height = 384

    def initiate(self, orientation = 1):
        if orientation == 1:
            self.width = 640
            self.height = 384
        else:
            self.width = 384
            self.height = 640
        self.clear()
        self.draw = ImageDraw.Draw(self.image)

    def write(self, text, fontSize, loc):
        font = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), fontSize)
        self.draw.text(loc, text, font = font, fill = 0)

    def setImage(self, imagefile, loc):
        img = Image.open(os.path.join(picdir, imagefile))
        self.image.paste(img, loc)

    def clear(self):
        self.image = Image.new('1', (self.width, self.height), 255)

    def getImg(self):
        return self.image

