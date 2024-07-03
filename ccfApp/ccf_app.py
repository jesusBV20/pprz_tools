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
PyQt GUI app. for centralized circular formations (CCF) employing guidance vector fields (GVF)

>>> from pathlib import Path
>>> hex_content = Path('icon.png').read_bytes()
>>> Path('icon.py').write_text(f'icon = {hex_content}')
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
    return app

def run_qml(app):
    engine = QQmlApplicationEngine()
    engine.addImportPath(Path(__file__).parent)
    engine.loadFromModule("control_panel", "Main")
    app.setWindowIcon(QIcon("penguin_icon_ccf.png"))

    if not engine.rootObjects():
        sys.exit(-1)

    return QCoreApplication.exec()
        
# -- If executed as a program --
if __name__ == '__main__':
    app = gen_app("CCF Control Panel")
    sys.exit(run_qml(app))