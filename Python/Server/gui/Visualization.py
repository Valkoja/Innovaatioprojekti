#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPainter, QPen, QRegion
from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot, QObject


class Visualization(QObject):
    def __init__(self, parent=None):
        #QQuickPaintedItem.__init__(self, parent)
        super().__init__()