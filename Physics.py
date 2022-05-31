import random

import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from typing import Tuple
from PyQt5.QtGui import QColor

import Globals

from Boid import Boid


Point = Tuple[float, float]
def t(p: QtCore.QPointF) -> Point:
    return p.x(), p.y()

class Physics(QtWidgets.QGraphicsRectItem): # Creation of the environment
    size = Globals.environmentSize
    extent = size / 2
    bounds = QtCore.QRectF(-extent, -extent, size, size)

    def __init__(self):
        super().__init__(self.bounds)
        self.setZValue(-10)

        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setItemIndexMethod(self.scene.NoIndex)
        self.boids = []
        self.scene.addItem(self)
        self.scene.setBackgroundBrush(QColor(0, 25, 60, 254))



        al = .5 * Boid.length
        self.scene.setSceneRect(Physics.bounds.adjusted(-al, -al, al, al))



    def add_boid(self, x, y, a): # "Adding boids" function
        boid = Boid(x, y, a)
        self.boids.append(boid)
        self.scene.addItem(boid)

    def add_boid_rnd(self): # "Adding randomly boids on the interface" function
        a = random.uniform(-Physics.extent,Physics.extent)
        r = random.uniform(-Physics.extent,Physics.extent)
        a2 = random.uniform(0, 359)
        self.add_boid(a, r, a2)

    def remove_boids(self): # "Removing boids" function
        last = self.boids[-1]
        self.scene.removeItem(last)
        del self.boids[-1]

    def step(self): # Binding "move" function and when the user clicks on the timer
        for a in self.boids:
            a.move(self)