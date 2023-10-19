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

from PySide6.QtCore import QObject, Property, Signal, Slot

class InfoDelta(QObject):

    value_changed = Signal()
    buffer_changed = Signal()
    id_from_changed = Signal()
    id_to_changed = Signal()

    def __init__(self, value, id_from, id_to) -> None:
        super().__init__()
        self._value = value
        self._buffer = value
        self._id_from = id_from
        self._id_to = id_to

    # ----- Indo Delta properties

    @Property(float, notify=value_changed)
    def value(self):
        return self._value
    
    @Property(float, notify=buffer_changed)
    def value_buffer(self):
        return self._buffer
    
    @Property(str, notify=id_from_changed)
    def id_from(self):
        return "{:03d}".format(self._id_from)
    
    @Property(str, notify=id_to_changed)
    def id_to(self):
        return "{:03d}".format(self._id_to)
    
    @value_buffer.setter
    def value_buffer(self, value):
        self._buffer = value
        self.buffer_changed.emit()

    # ---- Commit buffered delta value
    @Slot()
    def commit_delta(self):
        self._value = self._buffer
        self.value_changed.emit()
