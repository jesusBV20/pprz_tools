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
import json
import time
import numpy as np
from os import path, getenv, listdir

from info_ac import InfoAC
from info_delta import InfoDelta
from formationcontrol import FormationControlWorker
from log_reporter import LogReporter

from PySide6.QtCore import QObject, Property, Signal, Slot, QThread
from PySide6.QtQml import QmlElement, QmlSingleton

QML_IMPORT_NAME = "control_panel"
QML_IMPORT_MAJOR_VERSION = 1

MAIN_PATH = path.dirname(__file__)
JSON_FOLDER = path.join(MAIN_PATH, "formation")

PPRZ_HOME = getenv("PAPARAZZI_HOME")
PPRZ_SRC = getenv("PAPARAZZI_SRC")

sys.path.append(MAIN_PATH)
sys.path.append(PPRZ_HOME + "/var/lib/python/")
sys.path.append(PPRZ_SRC + "/sw/lib/python")

# --- PprzLink
from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from settings_xml_parse import PaparazziACSettings
# ---

"""\
This class will globally store the main configuration parameters.
"""
class ConfigCCF:
    def __init__(self):
        self.ac_info_list = []
        self.delta_info_list = []
        self.ccfstate = False

        # CCF controller parameters
        self.B = np.array([])
        self.k = 1.
        self.radius = 90.
        self.u_max = 20

        # CCF output
        self.u_list = np.array([])


"""\
Main application class which connects the frontend with the backend.
"""
@QmlElement
@QmlSingleton # The QML engine initialize this class
class ACPanel(QObject):

    json_file_changed = Signal()

    ac_info_updated = Signal()
    delta_info_updated = Signal()
    log_reporter_updated = Signal()

    ccfstate_changed = Signal()
    kccf_changed = Signal()
    umax_changed = Signal()

    def __init__(self) -> None:
        super().__init__()
        # Common config (ACPanel + CCF worker)
        self.conf = ConfigCCF()
        self.init_json_file()

        # ACPanel variables
        self.json_file = self._json_file
        self._ac_ids = []
        self._delta_list = [] # in deg!!

        # Start IVY Bus interface
        self._step = 1/10
        try:
            self.interface = IvyMessagesInterface("CCF Application")
            self.interface.subscribe(self.dl_values_cb, PprzMessage("telemetry", "DL_VALUE"))
            self.interface.subscribe(self.gvf_cb, PprzMessage("telemetry", "GVF"))
            self.interface.subscribe(self.navigation_cb, PprzMessage("telemetry", "NAVIGATION")) # fixedwing
            self.interface.subscribe(self.rotorcraft_fp_cb, PprzMessage("telemetry", "ROTORCRAFT_FP")) # rover/rotorcraft
        except:
            print("fail")
        
        # Log message
        self.log_reporter = LogReporter("INFO: Control Panel backend successfully initilized - ")

        # CCF worker
        self.ccf_worker = None
        self.ccf_thread = None

    def init_json_file(self):
        json_files = [f for f in listdir(JSON_FOLDER) if f.endswith('.json')]
        if not json_files:
            self._json_file = f"No .json files found in {JSON_FOLDER}"
        else:
            first_json_file = sorted(json_files)[0]
            self._json_file = first_json_file
            self._json_path = path.join(JSON_FOLDER, self._json_file)

    # ----- AC Panel properties

    @Property(str, constant=True)
    def json_main_folder(self):
        return JSON_FOLDER
    
    @Property(str, notify=json_file_changed)
    def json_file(self):
        return self._json_file
    
    @Property(str, notify=json_file_changed)
    def json_path(self):
        return self._json_path
    
    @Property("QVariant", notify=ac_info_updated)
    def ac_info_list(self):
        return self.conf.ac_info_list

    @Property("QVariant", notify=delta_info_updated)
    def delta_info_list(self):
        return self.conf.delta_info_list
    
    @Property(float, notify=kccf_changed)
    def k_ccf(self):
        return self.conf.k
    
    @Property(float, notify=umax_changed)
    def u_max(self):
        return self.conf.u_max
    
    @Property(bool, notify=ccfstate_changed)
    def ccfstate(self):
        return self.conf.ccfstate
    
    @Property(QObject, notify=ccfstate_changed)
    def reporter(self):
        return self.log_reporter


    # ----- AC Panel Property setters


    @json_file.setter
    def json_file(self, value):
        self._json_file = value
        self._json_path = path.join(JSON_FOLDER, self._json_file)
        self.json_file_changed.emit()

    @json_path.setter
    def json_path(self, value):
        self._json_path = value
        self._json_file = path.split(self._json_path)[-1]
        self.json_file_changed.emit()

    @k_ccf.setter
    def k_ccf(self, value):
        self.conf.k = value
        self.kccf_changed.emit()
        self.log_reporter.log("INFO: k_ccf={:.1f} successfully commited -".format(value))


    @u_max.setter
    def u_max(self, value):
        self.conf.u_max = value
        self.umax_changed.emit()
        self.log_reporter.log("INFO: u_max={:.1f} successfully commited -".format(value))


    # ----- AC Panel slots


    @Slot()
    def read_json_file(self):
        try:
            with open(self._json_path, 'r') as f:
                config = json.load(f) 

                self._ac_ids = config['ids']
                self._delta_list = config['desired_intervehicle_angles_degrees']
                self.conf.B = np.array(config['topology'])
                self.conf.k = config['gain']
                self.conf.radius = config['desired_stationary_radius_meters']
                self.conf.u_max = 0.2 * self.conf.radius
            self.kccf_changed.emit()
            self.umax_changed.emit()
            self.log_reporter.log("INFO: {:s} successfully loaded -".format(self._json_file))
        except:
            self.log_reporter.log("ERROR: error while loading {:s} -".format(self._json_path))

    @Slot()
    def ac_info_init(self):
        self.conf.ac_info_list = [InfoAC(i, self.log_reporter) for i in self._ac_ids]
        self.ac_info_updated.emit()

    @Slot()
    def delta_info_init(self):
        B = self.conf.B.T
        tmp_list = []
        for i in range(B.shape[0]):
            id_from = None
            id_to = None
            for j in range(B.shape[1]):
                if B[i,j] == -1:
                    id_from = self._ac_ids[j]
                if B[i,j] == 1:
                    id_to = self._ac_ids[j]
            
            tmp_list.append(InfoDelta(self._delta_list[i], id_from, id_to))
        
        self.conf.delta_info_list = tmp_list
        self.delta_info_updated.emit()

    @Slot()
    def commit_all_delta(self):
        for delta_info in self.conf.delta_info_list:
            delta_info.commit_delta() 
        self.log_reporter.log("INFO: delta values submitted -")


    # ----- Launching and stopping CCF

    # Switch the ccf_state
    def change_ccf_state(self):
        self.conf.ccfstate = not self.conf.ccfstate
        self.ccfstate_changed.emit()

    # After launch checks (check box, NAV and GVF status of every AC must be OK to launch CCF)
    def check_ac_states(self):
        if len(self.conf.ac_info_list) == 0:
            return False    
        
        for ac_info in self.conf.ac_info_list:
            ac = ac_info.ac
            if (not ac.info_checked):
                self.log_reporter.log("INFO: Waiting for check of AC-{:d} -".format(ac.id))
                return False
            if (not ac.initialized_nav) or (not ac.initialized_gvf):
                self.log_reporter.log("INFO: Waiting for NAV & GVF OK from AC-{:d} -".format(ac.id))
                return False
        return True

    # Run the previus checks before CCF launch
    @Slot()
    def try_launch_ccf(self):
        
        if self.ccf_thread is not None and self.conf.ccfstate == False:
            if self.ccf_thread.isRunning():
                self.log_reporter.log("ERROR: Wait for the last CCF thread to stop!! -")
                return
        
        if self.check_ac_states():
            self.change_ccf_state()
            if self.conf.ccfstate:
                self.launch_ccf()
        elif self.conf.ccfstate:
            self.change_ccf_state()

    # LAUNCH CCF!!
    def launch_ccf(self):
        self.ccf_thread = QThread()
        self.ccf_worker = FormationControlWorker(self.conf, self.log_reporter)
        self.ccf_worker.moveToThread(self.ccf_thread)

        self.ccf_thread.started.connect(self.ccf_worker.run)
        self.ccf_worker.progress.connect(self.commit_all_ac_rad)
        self.ccf_worker.finished.connect(self.ccf_thread.quit)
        
        self.ccf_thread.start() # Go Go Go!
        self.log_reporter.log("INFO: CCF thread created -")
    
    # STOP CCF!!
    @Slot()
    def stop_ccf(self):
        if self.conf.ccfstate:
            self.change_ccf_state()

    # Kill the CCF thread before closing
    @Slot()
    def kill_ccf_thread(self):
        if self.ccf_thread is not None:
            self.conf.ccfstate = False
            self.ccf_thread.quit()
            self.ccf_thread.wait()


    #####################################################
    # IVY BUS slots                                     #
    #####################################################
    
    @Slot()
    def stop_ivy_interface(self):
        self.interface.shutdown()

    # ######### MSG senders #########

    # Msg to request settings' value
    def get_dl_value(self, ac_id, msg_id):
        msg = PprzMessage("ground", "GET_DL_SETTING")
        msg['ac_id'] = ac_id
        msg["index"] = msg_id
        self.interface.send(msg)

    # Msg to send a new settings' value
    def send_dl_setting(self, ac_id, msg_id, value):
        msg = PprzMessage("ground", "DL_SETTING")
        msg['ac_id'] = ac_id
        msg['index'] = msg_id
        msg['value'] = value
        self.interface.send(msg)

    # ######### Commit slots #########

    @Slot(int)
    def get_ac_dl_values(self, ac_id):
        i = self._ac_ids.index(ac_id)

        self.conf.ac_info_list[i].ac.status = False
        self.conf.ac_info_list[i].ac_status_changed.emit()

        for msg_id in self.conf.ac_info_list[i].ac._settings_ids.values():
            self.get_dl_value(ac_id, msg_id)
            time.sleep(self._step)
        self.log_reporter.log("INFO: DL_VALUEs requested -")

    @Slot(int)
    def commit_settings(self, ac_id):
        i = self._ac_ids.index(ac_id)
        index_ell_ke = self.conf.ac_info_list[i].ac._settings_ids["ell_ke"]
        index_ell_kn = self.conf.ac_info_list[i].ac._settings_ids["ell_kn"]
        ke = self.conf.ac_info_list[i].buffer["ke"]
        kn = self.conf.ac_info_list[i].buffer["kn"]
        if ke is not None:
            self.send_dl_setting(ac_id, index_ell_ke, ke)
        if kn is not None:
            self.send_dl_setting(ac_id, index_ell_kn, kn)
        self.log_reporter.log("INFO: DL_SETTINGs commited -")

    @Slot()
    def commit_all_ac_rad(self):
        for ac_id in self._ac_ids:
            i = self._ac_ids.index(ac_id)
            u = self.conf.u_list[i]
            index_ell_a = self.conf.ac_info_list[i].ac._settings_ids["ell_a"]
            index_ell_b = self.conf.ac_info_list[i].ac._settings_ids["ell_b"]
            self.send_dl_setting(ac_id, index_ell_a, self.conf.radius + u)
            self.send_dl_setting(ac_id, index_ell_b, self.conf.radius + u)


    #####################################################
    # IVY BUS callbacks                                 #
    #####################################################

    # Process the DL_VALUE PprzMsg
    def dl_values_cb(self, ac_id, msg):
        if ac_id in self._ac_ids and msg.name == "DL_VALUE":
            i = self._ac_ids.index(ac_id)
            ac = self.conf.ac_info_list[i].ac

            msg_id = int(msg.get_field(0))
            if msg_id in ac._settings_ids.values():
                key = [k for k, v in ac._settings_ids.items() if v == msg_id]
                ac._settings[key[0]] = float(msg.get_field(1))
                self.conf.ac_info_list[i].ac_info_updated.emit()
                
                ac.status = True
                self.conf.ac_info_list[i].ac_status_changed.emit()

    # Process the NAVIGATION PprzMsg
    def navigation_cb(self, ac_id, msg):
        if ac_id in self._ac_ids and msg.name == "NAVIGATION":
            i = self._ac_ids.index(ac_id)
            ac = self.conf.ac_info_list[i].ac

            ac.XY[0] = float(msg.get_field(2))
            ac.XY[1] = float(msg.get_field(3))

            self.conf.ac_info_list[i].ac.time_last_nav = time.monotonic()
            self.conf.ac_info_list[i].set_initialized_nav(True)

    # 
    def rotorcraft_fp_cb(self, ac_id, msg):
        if ac_id in self._ac_ids and msg.name == "ROTORCRAFT_FP":
            i = self._ac_ids.index(ac_id)
            ac = self.conf.ac_info_list[i].ac
            
            ac.XY[0] = float(msg.get_field(0))/256
            ac.XY[1] = float(msg.get_field(1))/256

            self.conf.ac_info_list[i].ac.time_last_nav = time.monotonic()
            self.conf.ac_info_list[i].set_initialized_nav(True)

    # Process the GVF PprzMsg
    def gvf_cb(self, ac_id, msg):
        if ac_id in self._ac_ids and msg.name == "GVF":
            if int(msg.get_field(1)) == 1: # ELLIPSE trajectory
                i = self._ac_ids.index(ac_id)
                ac = self.conf.ac_info_list[i].ac

                param = msg.get_field(4)
                ac.XYc[0] = float(param[0])
                ac.XYc[1] = float(param[1])
                ac._settings["ell_a"] = float(param[2])
                ac._settings["ell_b"] = float(param[3])
                ac.s = float(msg.get_field(2))

                self.conf.ac_info_list[i].ac.time_last_gvf = time.monotonic()
                self.conf.ac_info_list[i].set_initialized_gvf(True)


            
