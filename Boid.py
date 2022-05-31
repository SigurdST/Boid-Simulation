import math
from random import *

import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtGui as QtGui
from PyQt5 import QtCore

import Globals
import Physics


class Boid(QtWidgets.QGraphicsItem): # Boid creation
    pixRect = None
    length = Globals.boidLength
    half_length = .5 * length
    width = 2 * length / 3
    bounds = QtCore.QRectF(-.5 * length, -.5 * width, length, width)

    @staticmethod
    def load_assets():
        Boid.pix = QtGui.QPixmap("poisson3.png") # fish picture (taken from the internet)
        Boid.pixRect = QtCore.QRectF(Boid.pix.rect())

    def boundingRect(self):
        return Individual.bounds

    # Draw method for an ant
    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.black)        # Plain (and ugly) black rectangle
        painter.drawRect(Ant.bounds)

    def __init__(self, x, y, a):
        super().__init__()
        self.setPos(x, y)
        self.setRotation(a)

    def boundingRect(self):
        return Boid.bounds

    def paint(self, painter, option, widget=None): # "Drawing a boid" function
        painter.drawPixmap(Boid.bounds, Boid.pix, Boid.pixRect)


    def move(self, physics): # "Boid moving" function
        a = self.rotation()
        ab = a+(uniform(-15, 15))
        p = Physics.t(self.pos())
        x, y = p
        s = 0
        m = 0
        for i in physics.boids: # Here, we look for boids close to a boid, to adapt its rotation
            pi = Physics.t(i.pos())
            xi, yi = pi
            if x != xi and y != yi:
                if xi - physics.extent / 10 <= x <= xi + physics.extent / 10 and yi - physics.extent / 10 <= y <= yi + physics.extent / 10:
                    s += 1
                    m += i.rotation()
        if s == 0:
            self.setRotation(ab)
        else:
            ri = m / s
            self.setRotation((ri+ab*6)/7)
        ar = math.pi * ab / 180
        if x == physics.extent:
            if y == physics.extent:
                self.setPos(-physics.extent + 1, -physics.extent + 1)
            if y == -physics.extent:
                self.setPos(-physics.extent + 1, physics.extent - 1)
            else:
                self.setPos(-physics.extent + 0.1, min(physics.extent, max(y - math.sin(ar), -physics.extent)))
        elif x == -physics.extent:
            if y == physics.extent:
                self.setPos(physics.extent - 1, -physics.extent + 1)
            if y == -physics.extent:
                self.setPos(physics.extent - 1, physics.extent - 1)
            else:
                self.setPos(physics.extent - 1, min(physics.extent, max(y - math.sin(ar), -physics.extent)))
        elif y == physics.extent:
            if x != physics.extent and x != -physics.extent:
                self.setPos(min(physics.extent, max(x - math.cos(ar), -physics.extent)), -physics.extent + 1)
        elif y == -physics.extent:
            if x != physics.extent and x != -physics.extent:
                self.setPos(min(physics.extent, max(x - math.cos(ar), -physics.extent)), physics.extent - 1)
        else:
            self.setPos(min(physics.extent, max(x - math.cos(ar), -physics.extent)),
                        min(physics.extent, max(y - math.sin(ar), -physics.extent)))
            
            '''See below the program to avoid collisions between boids (not working)
        p2 = Physics.t(self.pos())
        print(x)
        x2, y2 = p2
        for i in physics.boids:
            pi = Physics.t(i.pos())
            xi, yi = pi
            if x2 != xi and y2 != yi:
                b=True
                while b==True:
                while xi - Globals.boidLength/2 <= x2 <= xi + Globals.boidLength/2 and yi - Globals.boidLength/2 <= y2 <= yi + Globals.boidLength/2:
                    self.setPos(x, y)
                    a2 = a
                    a2 += (uniform(-45, 45))
                    ar2 = math.pi * a2 / 180
                    self.setRotation(a2)
                    self.setPos(min(physics.extent, max(x2 - math.cos(ar2), -physics.extent)),
                                min(physics.extent, max(y2 - math.sin(ar2), -physics.extent)))
                    p2 = Physics.t(self.pos())
                    x2, y2 = p2
                        #b=True
                    else:
                       b=False'''
