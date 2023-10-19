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

import sys
import numpy as np
from os import path, getenv

from PySide6.QtCore import QObject, Property, Signal, Slot

# --- PprzLink
PPRZ_HOME = getenv("PAPARAZZI_HOME", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
PPRZ_SRC = getenv("PAPARAZZI_SRC", path.normpath(path.join(path.dirname(path.abspath(__file__)), '../../../../')))
sys.path.append(PPRZ_HOME + "/var/lib/python/")
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from settings_xml_parse import PaparazziACSettings
from pprzlink.message import PprzMessage
# ---

class AC:
    def __init__(self, ac_id):
        self.id = ac_id
        self.status = True

        self.XY = np.zeros(2)
        self.XYc = np.zeros(2)
        self.s = 1
        self.sigma = 0

        self.initialized_gvf = False
        self.initialized_nav = False
        self.info_checked = False

        # Setting to be modified
        self._settings_ids = {"ell_a":None, "ell_b":None, "ell_ke":None, "ell_kn":None}
        self._settings = {"ell_a":None, "ell_b":None, "ell_ke":None, "ell_kn":None}

        # System time of last received messages
        self.time_last_nav = None
        self.time_last_gvf = None

class InfoAC(QObject):

    ac_changed = Signal()
    ac_status_changed = Signal()
    ac_info_updated = Signal()
    ac_settings_updated = Signal()
    ac_nav_state_changed = Signal()
    ac_gvf_state_changed = Signal()
    ac_check_changed = Signal()

    def __init__(self, ac_id, log_reporter) -> None:
        super().__init__()
        self.ac = AC(ac_id)
        self.buffer = {"ke":None, "kn":None}
        self.log_reporter = log_reporter
        
        self.look_setting_ids()

    def set_initialized_nav(self, state):
        self.ac.initialized_nav = state
        self.ac_nav_state_changed.emit()

    def set_initialized_gvf(self, state):
        self.ac.initialized_gvf = state
        self.ac_gvf_state_changed.emit()

    # ----- AC Info properties

    @Property(int, notify=ac_changed)
    def id(self):
        return self.ac.id
    
    @Property(str, notify=ac_changed)
    def idLabel(self):
        return "{:03d}".format(self.ac.id)
      
    @Property(bool, notify=ac_status_changed)
    def status(self):
        return self.ac.status
    
    # Info values...
    @Property(str, notify=ac_info_updated)
    def ell_a(self):
        if self.ac._settings["ell_a"] is None:
            return "-"
        else:
            return "{:.1f}".format(self.ac._settings["ell_a"])
    
    @Property(str, notify=ac_info_updated)
    def ell_b(self):
        if self.ac._settings["ell_b"] is None:
            return "-"
        else:
            return "{:.1f}".format(self.ac._settings["ell_b"])
    
    # Flags...
    @Property(bool, notify=ac_nav_state_changed)
    def nav_state(self):
        return self.ac.initialized_nav
    
    @Property(bool, notify=ac_gvf_state_changed)
    def gvf_state(self):
        return self.ac.initialized_gvf

    @Property(bool, notify=ac_check_changed)
    def info_checked(self):
        return self.ac.info_checked

    # Settings...
    @Property(float, notify=ac_info_updated)
    def ke(self):
        return self.ac._settings["ell_ke"]
    
    @Property(float, notify=ac_info_updated)
    def kn(self):
        return self.ac._settings["ell_kn"]
    

    # ---- Info AC setters


    @status.setter
    def status(self, value):
        self.ac.status = value
        self.ac_status_changed.emit()

    @ke.setter
    def ke(self, value):
        self.buffer["ke"] = value

    @kn.setter
    def kn(self, value):
        self.buffer["kn"] = value


    # ---- Info AC slots


    # Get settings idexes
    Slot()
    def look_setting_ids(self):
        settings = PaparazziACSettings(self.ac.id)
        for setting_ in self.ac._settings_ids.keys():
                try:
                    index = settings.name_lookup[setting_].index
                    if setting_ == 'ell_a':
                        self.ac._settings_ids["ell_a"] = index
                    if setting_ == 'ell_b':
                        self.ac._settings_ids["ell_b"] = index
                    if setting_ == 'ell_ke':
                        self.ac._settings_ids["ell_ke"] = index
                    if setting_ == 'ell_kn':
                        self.ac._settings_ids["ell_kn"] = index
                except Exception as e:
                    print(e)
                    self.log_reporter.log("ERROR: AC-" + self.idLabel + " reported " + setting_ + \
                                          " setting not found. Have you forgotten to check gvf.xml for your settings? -")
    
    # Try to change de info checked flag
    @Slot()
    def change_info_checked(self):
        if None in self.ac._settings.values():
            self.log_reporter.log("INFO: All DL_VALUEs of the AC-" + self.idLabel + \
                                  " are required for the user to be able to verify a check -")
            return
        
        self.ac.info_checked = not self.ac.info_checked
        self.ac_check_changed.emit()

