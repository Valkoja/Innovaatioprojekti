#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from PyQt5.QtQuick import QQuickPaintedItem
from PyQt5.QtSvg import QSvgRenderer

import math, svgutils

class SVGView(QQuickPaintedItem):
    def __init__(self, parent = None):
        super().__init__(self, parent)
        self.orgBoom = svgutils.compose.SVG('./gui/svg/boom.svg')


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
        qp = painter

        newBoom = self.orgBoom
        newBoom.rotate(30, 500, 500)
        #newBoom.move(200, 300)

        compose = svgutils.compose.Figure(1000, 1000, newBoom)
        svg = QSvgRenderer(compose.tostr())
        svg.render(qp)

    '''
        # Selvitä nämä
        # self.setOpaquePainting(False)
        # self.setTextureSize = QSize(600, 600)

        # Puomin kulma ja koordinaatit
        boomA = 60
        boomX = 550
        boomY = 475

        # Toisen puomin kulma ja koordinaatit
        armA = 40
        armX = boomX + self.calculateX(boomA, 385)
        armY = boomY + self.calculateY(boomA, 385)

        # Kauhan kulma ja koordinaatit
        bucketA = 20
        bucketX = armX + self.calculateX(boomA + armA, 176)
        bucketY = armY + self.calculateY(boomA + armA, 176)
    '''