#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtSvg import QSvgRenderer

import math, svgutils

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


    def resizeEvent(self, event):
        self.update()


    def paint(self, painter):
        # qp = painter

        # Puomin alkupisteen koordinaatit
        boomX = 900
        boomY = 900

        boomSVG = self._boomSVG
        boomSVG.rotate(self._boomAngle, 500, 500)
        boomSVG.move(boomX - 500, boomY - 500)

        # Toinen puomi
        armX = boomX + self.calculateX(self._boomAngle, 385)
        armY = boomY + self.calculateY(self._boomAngle, 385)

        armSVG = self._armSVG
        armSVG.rotate(self._boomAngle + self._armAngle, 500, 500)
        armSVG.move(armX - 500, armY - 500)

        # Kauha
        bucketX = armX + self.calculateX(self._boomAngle + self._armAngle, 176)
        bucketY = armY + self.calculateY(self._boomAngle + self._armAngle, 176)

        bucketSVG = self._bucketSVG
        bucketSVG.rotate(self._boomAngle + self._armAngle + self._bucketAngle, 500, 500)
        bucketSVG.move(bucketX - 500, bucketY - 500)

        # Yhdistetään
        compose = svgutils.compose.Figure('1000px', '1000px', boomSVG, armSVG, bucketSVG)
        svg = QSvgRenderer(compose.move(-200, -200).scale(1.2).tostr())
        svg.render(painter)

        print(self._boomAngle)
        print(self._armAngle)
        print(self._bucketAngle)


    '''
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