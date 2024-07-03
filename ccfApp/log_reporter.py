#!/usr/bin/env python
#
# Copyright (C) 2023 Jesús Bautista Villar <jesbauti20@gmail.com>
#                    Hector Garcia de Marina <hgdemarina@gmail.com>
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

from PySide6.QtCore import QObject, Signal, Property, Slot

class LogReporter(QObject):
    
    console_log_changed = Signal()

    def __init__(self, init_msg=""):
        super().__init__()
        self.last_log = init_msg
        self.full_log = init_msg
        self.console_log_changed.emit()

    @Property(str, notify=console_log_changed)
    def console_log(self):
        return self.full_log

    @Slot(str)
    def log(self, msg):
        if self.last_log is None:
            self.full_log = self.full_log + msg
        else:
            self.full_log = self.full_log + "\n" + msg
        self.last_log = msg
        self.console_log_changed.emit()