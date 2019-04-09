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
        self._slopeAngle = 0
        self._heightFromZero = 0
        self._heightFromSlope = 0
        self._distanceFromZero = 0


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

        # Zero level
        # self._levelList.pop(0)
        # self._levelList.append(self._heightToSlopeFromZero + self._heightFromZero)

        levelX = bucketX + self.calculateX(bucketA, 136)
        levelY = bucketY + self.calculateY(bucketA, 136) + self._heightToSlopeFromZero + self._heightFromZero
        # levelY = bucketY + self.calculateY(bucketA, 136) + sum(self._levelList) / 10

        if self._levelSlope != 0:
            levelA = (self._levelSlope / 100) * 45
            levelA = round(math.degrees(levelA), 1)
            levelSVG.rotate(levelA, 1000, 1000)

        levelSVG.move(levelX - 1000, levelY - 1000)

        # Combine pieces into one
        compose = svgutils.compose.Figure('1000px', '1000px', levelSVG, boomSVG, armSVG, bucketSVG)

        # Set scale based on system we're running on due to DPI weirdness
        if platform.system() == 'Darwin':
            scale = 0.6
            moveX = -200 # Despite scale, same as in win / linux
            moveY = -200 # pending further investigation
        else:
            scale = 1.2
            moveX = -200
            moveY = -200

        # Do we need to compensate for position, eg. original moved -200 -200 for 1.2 scale
        image = compose.move(moveX, moveY).scale(scale).tostr()

        # Hacky wacky to make Qt not crash and burn about encoding
        imageStr = image.decode('utf-8')
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
        return self._heightFromZero


    @heightFromZero.setter
    def heightFromZero(self, heightFromZero):
        self._heightFromZero = heightFromZero * 100 # Meters to centimeters


    @pyqtProperty(float)
    def heightFromSlope(self):
        return self._heightFromSlope


    @heightFromSlope.setter
    def heightFromSlope(self, heightFromSlope):
        self._heightFromSlope = heightFromSlope * 100 # Meters to centimeters


    @pyqtProperty(float)
    def distanceFromZero(self):
        return self._distanceFromZero


    @distanceFromZero.setter
    def distanceFromZero(self, distanceFromZero):
        self._distanceFromZero = distanceFromZero * 100 # Meters to centimeters


    @pyqtProperty(float)
    def slopePercent(self):
        return (self._slopeAngle / 90) * 45


    @slopePercent.setter
    def slopePercent(self, slopePercent):
        self._slopeAngle = (slopePercent / 45) * 90


    @pyqtSlot()
    def reDraw(self):
        self.update()