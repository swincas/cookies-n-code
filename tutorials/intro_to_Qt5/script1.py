# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 00:40:02 2019

@author: 1313e
"""

# %% SCRIPT 1
from qtpy import QtCore as QC, QtWidgets as QW

# Create Qt application instance
app = QW.QApplication.instance()
if app is None:
    app = QW.QApplication([])

# Create main window
main_window = QW.QMainWindow()

# Create text label
label = QW.QLabel("Hello World!")
label.setAlignment(QC.Qt.AlignCenter)

# Set label as central widget
main_window.setCentralWidget(label)

# Show main window
main_window.show()

# Start Qt event loop
app.exec_()
