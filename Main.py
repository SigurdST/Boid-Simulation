import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import Qt
import PyQt5.QtGui as QtGui
from PyQt5.QtWidgets import QLabel

import Globals
import Misc
import Physics
from Boid import Boid

import random

random.seed(2531)


def theme_icon(name):
    return QtGui.QIcon.fromTheme(name)

def build_buttons_panel(timer): # We create play/stop, skip buttons

    controls = QtWidgets.QHBoxLayout()
    controls.addStretch(1)

    b_pause = QtWidgets.QToolButton()
    b_pause.setShortcut("Space")
    b_pause.setIcon(QtGui.QIcon('play.png'))
    controls.addWidget(b_pause)

    b_step = QtWidgets.QToolButton()
    b_step.setShortcut("N")
    b_step.setIcon(QtGui.QIcon('skip.png'))
    controls.addWidget(b_step)

    controls.addStretch(1)

    # Setting play/pause
    def maybe_run(): # Modify the play/stop button when we click on it
        if timer.isActive():
            timer.stop()
            b_pause.setIcon(QtGui.QIcon('play.png'))
        else:
            timer.start(1000 // 25)
            b_pause.setIcon(QtGui.QIcon('pause.png'))

    b_pause.clicked.connect(maybe_run)

    b_step.clicked.connect(physics.step)

    return controls


def build_configuration_panel(): # Create a slider to modify the number of boids
    layout = QtWidgets.QFormLayout()

    l_boid_count: QLabel = QtWidgets.QLabel(str(Globals.boidCount))
    layout.addRow("Boids", l_boid_count)

    s_boid_count = QtWidgets.QSlider(Qt.Horizontal)
    s_boid_count.setMinimum(1)
    s_boid_count.setMaximum(200)
    layout.addRow("", s_boid_count)
    s_boid_count.setValue(Globals.boidCount)

    def update_boids_counts(count): # "Modifying the number of boids" function (when we use the timer)
        while count != len(physics.boids):
            for i in range(len(physics.boids)):
                physics.remove_boids()
            for i in range(count):
                physics.add_boid_rnd()
        l_boid_count.setText(str(len(physics.boids)))

    s_boid_count.valueChanged.connect(update_boids_counts)

    return layout


def build_control_panel(timer):
    holder = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout()
    layout.addLayout(build_buttons_panel(timer))
    layout.addLayout(build_configuration_panel())
    holder.setLayout(layout)
    return holder


app = QtWidgets.QApplication([])
physics = Physics.Physics()
view = Misc.AutoscaledGraphicsView(physics.scene)

# We add a timer
q_timer = QtCore.QTimer()
q_timer.timeout.connect(physics.step)

# Boid creation
Boid.load_assets()
for i in range(Globals.boidCount):
    physics.add_boid_rnd()

# Boid moving

if __name__ == '__main__':
    w = QtWidgets.QMainWindow()
    splitter = QtWidgets.QSplitter(Qt.Horizontal)
    splitter.addWidget(view)
    splitter.addWidget(build_control_panel(q_timer))
    w.setCentralWidget(splitter)
    w.setWindowTitle("Boids")
    w.show()

    app.exec()