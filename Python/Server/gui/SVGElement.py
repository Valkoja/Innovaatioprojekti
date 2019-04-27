#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, QRect, QSize, QPointF
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtSvg import QSvgRenderer

import math, svgutils, copy, platform

class SVGElement(QQuickPaintedItem):
    def __init__(self, parent = None):
        super().__init__(self, parent)
        self.setOpaquePainting(False)

        self._boomSVG = svgutils.compose.SVG('./gui/svg/boom.svg')
        self._boomSin = [math.sin(math.radians(40)) for i in range(10)]
        self._boomCos = [math.cos(math.radians(40)) for i in range(10)]
        self._boomAngle = 0

        self._armSVG = svgutils.compose.SVG('./gui/svg/arm.svg')
        self._armSin = [math.sin(math.radians(-60)) for i in range(10)]
        self._armCos = [math.cos(math.radians(-60)) for i in range(10)]
        self._armAngle = 0

        self._bucketSVG = svgutils.compose.SVG('./gui/svg/bucket.svg')
        self._bucketSin = [math.sin(math.radians(-150)) for i in range(10)]
        self._bucketCos = [math.cos(math.radians(-150)) for i in range(10)]
        self._bucketAngle = 0

        self._levelSVG = svgutils.compose.SVG('./gui/svg/level.svg')
        self._levelX = None
        self._levelY = None
        self._levelA = 0

        self._heightFromZero = None
        self._distanceFromZero = None


    def calculateX(self, aAngle, aLength):
        x = math.floor(math.fabs(math.cos(math.radians(aAngle)) * aLength))

        if -90 <= aAngle <= 90:
            x = x * -1
        
        return x


    def calculateY(self, aAngle, aLength):
        y = math.floor(math.fabs(math.sin(math.radians(aAngle)) * aLength))
        
        if 0 <= aAngle <= 180:
            y = y * -1
        
        return y


    def calculateA(self, aSinList, aCosList):
        s = sum(aSinList)
        c = sum(aCosList)
        a = math.atan2(s, c)

        return round(math.degrees(a), 1)


    def paint(self, painter):
        boomSVG = copy.deepcopy(self._boomSVG)
        armSVG = copy.deepcopy(self._armSVG)
        bucketSVG = copy.deepcopy(self._bucketSVG)
        levelSVG = copy.deepcopy(self._levelSVG)

        # Boom
        self._boomSin.pop(0)
        self._boomCos.pop(0)
        self._boomSin.append(math.sin(math.radians(self._boomAngle)))
        self._boomCos.append(math.cos(math.radians(self._boomAngle)))

        boomA = self.calculateA(self._boomSin, self._boomCos)
        boomX = 900
        boomY = 900

        boomSVG.rotate(boomA, 500, 500)
        boomSVG.move(boomX - 500, boomY - 500)

        # Digging arm
        self._armSin.pop(0)
        self._armCos.pop(0)
        self._armSin.append(math.sin(math.radians(self._armAngle)))
        self._armCos.append(math.cos(math.radians(self._armAngle)))

        armA = self.calculateA(self._armSin, self._armCos)
        armX = boomX + self.calculateX(boomA, 385)
        armY = boomY + self.calculateY(boomA, 385)

        armSVG.rotate(armA, 500, 500)
        armSVG.move(armX - 500, armY - 500)

        # Bucket
        self._bucketSin.pop(0)
        self._bucketCos.pop(0)
        self._bucketSin.append(math.sin(math.radians(self._bucketAngle)))
        self._bucketCos.append(math.cos(math.radians(self._bucketAngle)))

        bucketA = self.calculateA(self._bucketSin, self._bucketCos)
        bucketX = armX + self.calculateX(armA, 176)
        bucketY = armY + self.calculateY(armA, 176)

        bucketSVG.rotate(bucketA, 500, 500)
        bucketSVG.move(bucketX - 500, bucketY - 500)

        # Zero level, calculated without hysteresis for accuracy and combining svg:s into one
        if self._heightFromZero is not None and self._distanceFromZero is not None:
            if self._levelX is None or self._levelY is None:
                self._levelX = 900 + self.calculateX(self._boomAngle, 385) + self.calculateX(self._armAngle, 176) + self.calculateX(self._bucketAngle, 136) + self._distanceFromZero
                self._levelY = 900 + self.calculateY(self._boomAngle, 385) + self.calculateY(self._armAngle, 176) + self.calculateY(self._bucketAngle, 136) + self._heightFromZero

            levelSVG.rotate(self._levelA, 1000, 1000)
            levelSVG.move(self._levelX - 1000, self._levelY - 1000)

            # Ignore level if it is not set
            compose = svgutils.compose.Figure('1000px', '1000px', levelSVG, boomSVG, armSVG, bucketSVG)
        else:
            compose = svgutils.compose.Figure('1000px', '1000px', boomSVG, armSVG, bucketSVG)

        # Set scale based on system we're running on due to DPI weirdness
        if platform.system() == 'Darwin':
            scale = 0.6
            moveX = -200 # Despite different scale, same as in
            moveY = -200 # win / linux, pending further investigation
        else:
            scale = 1.2
            moveX = -200
            moveY = -200

        # Hacky wacky to make Qt not crash and burn about encoding
        imageStr = compose.move(moveX, moveY).scale(scale).tostr().decode('utf-8')
        imageStr = imageStr.replace("encoding='ASCII'", "encoding='UTF-8'")
        imageStr = imageStr.encode('utf-8')

        svg = QSvgRenderer(imageStr)
        svg.render(painter)


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


    @pyqtProperty(float)
    def heightFromZero(self):
        # Centimeters back to meters
        return self._heightFromZero / 100


    @heightFromZero.setter
    def heightFromZero(self, heightFromZero):
        # Meters to centimeters
        self._heightFromZero = heightFromZero * 100


    @pyqtProperty(float)
    def distanceFromZero(self):
        # Centimeters back to meters
        return self._distanceFromZero / 100


    @distanceFromZero.setter
    def distanceFromZero(self, distanceFromZero):
        # Meters to centimeters
        self._distanceFromZero = distanceFromZero * 100


    @pyqtProperty(float)
    def slopePercent(self):
        # Degrees back to percents, 45 deg is 100 %
        return (self._levelA / 45) * 100


    @slopePercent.setter
    def slopePercent(self, slopePercent):
        # Percents to degrees, 100 % is 45 deg
        self._levelA = (slopePercent / 100) * 45


    @pyqtSlot()
    def reDraw(self):
        self.update()


    @pyqtSlot()
    def reLevel(self):
        self._levelX = None
        self._levelY = None
        self._heightFromZero = None
        self._distanceFromZero = None