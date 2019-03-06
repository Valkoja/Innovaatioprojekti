#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, QRect, QSize, QPointF
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtSvg import QSvgRenderer

import math, svgutils, copy


class SVGElement(QQuickPaintedItem):
    def __init__(self, parent = None):
        super().__init__(self, parent)
        self.setOpaquePainting(False)

        self._boomSVG = svgutils.compose.SVG('./gui/svg/boom.svg')
        self._boomAngle = 0
        self._armSVG = svgutils.compose.SVG('./gui/svg/arm.svg')
        self._armAngle = 0
        self._bucketSVG = svgutils.compose.SVG('./gui/svg/bucket.svg')
        self._bucketAngle = 0

    def calculateX(self, angle, length):
        x = math.floor(math.fabs(math.cos(math.radians(angle)) * length))

        if -90 <= angle <= 90:
            x = x * -1
        
        return x

    def calculateY(self, angle, length):
        y = math.floor(math.fabs(math.sin(math.radians(angle)) * length))
        
        if 0 <= angle <= 180:
            y = y * -1
        
        return y

    def paint(self, painter):
        boomSVG = copy.deepcopy(self._boomSVG)
        armSVG = copy.deepcopy(self._armSVG)
        bucketSVG = copy.deepcopy(self._bucketSVG)

        # Boom
        boomX = 900
        boomY = 900

        boomSVG.rotate(self._boomAngle, 500, 500)
        boomSVG.move(boomX - 500, boomY - 500)

        # Digging arm
        armX = boomX + self.calculateX(self._boomAngle, 385)
        armY = boomY + self.calculateY(self._boomAngle, 385)

        armSVG.rotate(self._armAngle, 500, 500)
        armSVG.move(armX - 500, armY - 500)

        # Bucket
        bucketX = armX + self.calculateX(self._armAngle, 176)
        bucketY = armY + self.calculateY(self._armAngle, 176)

        bucketSVG.rotate(self._bucketAngle, 500, 500)
        bucketSVG.move(bucketX - 500, bucketY - 500)

        # Combine
        compose = svgutils.compose.Figure('1000px', '1000px', boomSVG, armSVG, bucketSVG)

        # Set scale based on system we're running on due to DPI weirdness
        import platform

        # Do we need to compensate for position, eg. original moved -200 -200 for 1.2 scale

        if platform.system() == 'Darwin':
            scale = 0.6
        else:
            scale = 1.2

        image = compose.move(-200, -200).scale(scale).tostr()

        # Hacky wacky to make Qt not crash and burn about encoding
        imagestring = image.decode('utf-8')
        imagestring = imagestring.replace("encoding='ASCII'", "encoding='UTF-8'")
        imagestring = imagestring.encode('utf-8')

        svg = QSvgRenderer(imagestring)
        svg.render(painter)

    '''
        # Debug
        print(self._boomAngle)
        print(self._armAngle)
        print(self._bucketAngle)

        # Vanhoja?
        self.setOpaquePainting(False)
        self.setTextureSize = QSize(600, 600)

        # Elementin koko
        print(str(self.width()))
        print(str(self.height()))
    '''


    @pyqtProperty(int)
    def boomAngle(self):
        return self._boomAngle


    @boomAngle.setter
    def boomAngle(self, boomAngle):
        self._boomAngle = boomAngle


    @pyqtProperty(int)
    def armAngle(self):
        return self._armAngle


    @armAngle.setter
    def armAngle(self, armAngle):
        self._armAngle = armAngle


    @pyqtProperty(int)
    def bucketAngle(self):
        return self._bucketAngle


    @bucketAngle.setter
    def bucketAngle(self, bucketAngle):
        self._bucketAngle = bucketAngle


    @pyqtSlot()
    def reDraw(self):
        self.update()
