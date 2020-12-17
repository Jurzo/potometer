#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')

import logging
from waveshare_epd import epd7in5
import time
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

class Screen:
    width = 640
    height = 384

    def __init__(self):
        try:
            self.epd = epd7in5.EPD()
            logging.info("init and Clear")
            self.epd.init()
            self.epd.Clear()
            time.sleep(6)
        except IOError as e:
            logging.info(e)

    def draw(self, image):
        self.epd.display(self.epd.getbuffer(image))
        time.sleep(6)

    def clear(self):
        logging.info("White screen")
        image = Image.new('1', (self.epd.width, self.epd.height), 255)  # 255: clear the frame
        self.epd.display(self.epd.getbuffer(image))
        time.sleep(6)

    def exit(self):
        self.epd.init()
        self.epd.Clear()
        logging.info("Goto Sleep...")
        self.epd.sleep()
        self.epd.Dev_exit()
        epd7in5.epdconfig.module_exit()