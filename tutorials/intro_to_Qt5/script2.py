# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:40:02 2019

@author: 1313e
"""

# %% SCRIPT 2
from qtpy import QtWidgets as QW

# Create Qt application instance
app = QW.QApplication.instance()
if app is None:
    app = QW.QApplication([])

# Create main window
main_window = QW.QMainWindow()

# Create central widget and set it
widget = QW.QWidget()
main_window.setCentralWidget(widget)

# Create layout for central widget and set it
layout = QW.QHBoxLayout()
widget.setLayout(layout)

# Create button and add to layout
button = QW.QPushButton("Hello World!")
layout.addWidget(button)

# Show main window
main_window.show()

# Start Qt event loop
app.exec_()
