#!/usr/bin/env python
#
# Copyright (C) 2023 Jesús Bautista Villar <jesbauti20@gmail.com>
#
# This file is part of paparazzi.
#
# paparazzi is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# paparazzi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with paparazzi; see the file COPYING.  If not, see
# <http://www.gnu.org/licenses/>.

"""\
PySide6 GUI app. for centralized circular formations (CCF) employing guidance vector fields (GVF)

https://doc.qt.io/qtforpython-6/examples/example_corelib_threads.html
https://doc.qt.io/qtforpython-6/examples/example_bluetooth_lowenergyscanner.html
https://doc.qt.io/qt-6/qtquickcontrols-customize.html#customizing-slider
https://realpython.com/python-pyqt-qthread/
"""

import sys
from pathlib import Path

from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from acpanel import ACPanel

def gen_app(name):
    app = QGuiApplication(sys.argv)
    QCoreApplication.setApplicationName(name)
    app.setWindowIcon(QIcon("CCF_ControlPanel/assets/appIcon.png"))
    return app

def run_qml(app):
    engine = QQmlApplicationEngine()
    engine.addImportPath(Path(__file__).parent)
    engine.loadFromModule("CCF_ControlPanel", "Main")
    app.setWindowIcon(QIcon("CCF_ControlPanel/assets/app_icon.png"))

    if not engine.rootObjects():
        sys.exit(-1)

    return QCoreApplication.exec()
        
# -- If executed as a program --
if __name__ == '__main__':
    app = gen_app("CCF Control Panel")
    sys.exit(run_qml(app))