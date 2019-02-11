#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import math

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QRegion
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot
from PyQt5.QtQuick import QQuickPaintedItem


class PiirtoQML(QQuickPaintedItem):
    def __init__(self, parent=None):
        QQuickPaintedItem.__init__(self, parent)
        self.setOpaquePainting(False)
        self.setTextureSize = QSize(600, 600)

        self.p1 = {'x': 0, 'y': 0}
        self.p2 = {'x': 0, 'y': 0}
        self.p3 = {'x': 0, 'y': 0}
        self.p4 = {'x': 0, 'y': 0}
        
        self.rPen = QPen(Qt.red, 3)
        self.gPen = QPen(Qt.green, 3)
        self.bPen = QPen(Qt.blue, 3)
        #self.setAngles(60, -90, -120)

    @pyqtSlot(float, float, float)
    def setAngles(self, a, b, c):
        self.p1['x'] = 550

        self.p1['y'] = 475
        
        # Puomi
        self.p2['x'] = self.p1['x'] + self.calculateX(a, 385)
        self.p2['y'] = self.p1['y'] + self.calculateY(a, 385)
        
        # Toinen puomi (?)
        self.p3['x'] = self.p2['x'] + self.calculateX(a + b, 176)
        self.p3['y'] = self.p2['y'] + self.calculateY(a + b, 176)
        
        # Kauha
        self.p4['x'] = self.p3['x'] + self.calculateX(a + b + c, 133)
        self.p4['y'] = self.p3['y'] + self.calculateY(a + b + c, 133)
        
        # Kutsutaan piirtoa
        self.update()

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
        #qp.begin(self)

        # Puomi
        qp.setPen(self.rPen)
        qp.drawLine(self.p1['x'], self.p1['y'], self.p2['x'], self.p2['y'])
        
        # Toinen puomi (?)
        qp.setPen(self.gPen)
        qp.drawLine(self.p2['x'], self.p2['y'], self.p3['x'], self.p3['y'])
        
        #Kauha
        qp.setPen(self.bPen)
        qp.drawLine(self.p3['x'], self.p3['y'], self.p4['x'], self.p4['y'])
        
        # Astetekstit?
        #qp.setPen(QColor(168, 34, 3))
        #qp.setFont(QFont('Decorative', 10))
        #qp.drawText(event.rect(), Qt.AlignCenter, self.text)    
        #self.drawText(event, qp)
        
        #qp.end()