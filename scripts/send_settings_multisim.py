#!/usr/bin/env python
#
# Copyright (C) 2022 Jesús Bautista Villar <jesbauti20@gmail.com>
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
#

'''
Building in progress python script to send a stack of SETTING and BLOCK 
datalink messages. It has been designed to initialise the GVF multiple 
agents nps simulations.

Usage example: 
    ./send_multisim_settings.py -ad_ids 5,6,7 -v
'''

import sys
from os import path, getenv
from time import sleep

import numpy as np

PPRZ_HOME = getenv("PAPARAZZI_HOME")
PPRZ_SRC = getenv("PAPARAZZI_SRC")

sys.path.append(PPRZ_HOME + "/var/lib/python/")
sys.path.append(PPRZ_SRC + "/sw/lib/python")

from pprzlink.ivy import IvyMessagesInterface
from pprzlink.message import PprzMessage
from settings_xml_parse import PaparazziACSettings
import pprzlink.udp

DEFAULT_ADDRESS = "127.0.0.1"

# GCS ID, OUT port, IN port
gcs_conf = [0, DEFAULT_ADDRESS, 4243, 4242]

class Aircraft:
    def __init__(self, ac_id):
        self.id = ac_id
        self.settings = PaparazziACSettings(ac_id).name_lookup.copy() # It's a dictionary   

class settings_sender:
    def __init__(self, ac_ids):
        self.ac_ids = ac_ids

        try:
            self.aircrafts = [Aircraft(id) for id in self.ac_ids]

        except Exception as e:
            print(e)
            print("Error while loading PaparazziACSettings")

        # Start IVY interface
        self.interface = IvyMessagesInterface("Settings Sender")
        

    def new_ac(self, ac_id):
        self.ac_ids.append(ac_id)
        self.aircrafts.append(Aircraft(ac_id))
    

    def settings(self, ac_ids = None):
        if (ac_ids == None):
            ac_ids = self.ac_ids

        for ac in self.aircrafts:
            print("\n ----------------------- ")
            print(  "   ac " + str(ac.id) + " settings")
            print(  " ----------------------- ")

            for setting in ac.settings:
                print(str(ac.settings[setting].index) + "-> \'" + setting + "\'")


    def send_setting(self, ac_id, index, value):
        sleep(0.1)
        if (self.interface == None):
            return False

        if type(index) == str:
            for ac in self.aircrafts:
                if ac.id in ac_ids:
                    index = ac.settings[index].index
                    break

        if ac_id in self.ac_ids:
            msga = PprzMessage("datalink", "SETTING")
            msga["ac_id"] = ac_id
            msga['index'] = index
            msga['value'] = value
            self.interface.send(msga)
            print("Message sent to %i : %s" % (ac_id, str(msga)))
            return True
        else:
            print("send_setting: The ac_id " + str(ac_id) + " is not initialised")
            return False
        

    def send_block(self, ac_id, block_id):
        if (self.interface == None):
            return False

        if ac_id in self.ac_ids:
            msga = PprzMessage("datalink", "BLOCK")
            msga["ac_id"] = ac_id
            msga['block_id'] = block_id
            self.interface.send(msga)
            print("Message sent to %i : %s" % (ac_id, str(msga)))
            return True
        else:
            print("send_block: The ac_id " + str(ac_id) + " is not initialised")
            return False


    def stop(self):
        # Stop IVY interface
        if self.interface is not None:
            self.interface.shutdown()


    def __del__(self):
        self.stop()



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Circular formation")
    parser.add_argument('-ac_ids', '--ac_ids', dest='ac_ids', type=str, default=None, help="init ac_ids for the sender")
    parser.add_argument('-s', '--s', dest='show_settings', action='store_true', help="show init ACs settings")

    # CBF param arguments
    parser.add_argument('-gamma', '--gamma', dest='gamma', type=float, default=0.4, help="CBF param: collision radius")
    parser.add_argument('-col_rad', '--col_rad', dest='col_rad', type=float, default=2.0, help="CBF param: collision radius")
    # ---

    args = parser.parse_args()
    
    # Script parameters and setting
    ac_ids = args.ac_ids
    show_settings = args.show_settings

    ke, kn = 1, 1
    gamma = args.gamma
    col_rad = args.col_rad
    block_id = 3

    kp = 500
    speeds = [1, 2, 3]
    # ---
    
    if ac_ids is not None:
        ac_ids = ac_ids.split(",")
        ac_ids = [int(id) for id in ac_ids]

        sender = settings_sender(ac_ids)

        if show_settings:
            sender.settings()
            print(  " ----------------------- \n")
        
        # Send settings
        
        sleep(0.6)
        for ac_id, speed in zip(ac_ids, speeds):
            sender.send_setting(ac_id, "ell_ke", ke)
            sender.send_setting(ac_id, "ell_kn", kn)

            sender.send_setting(ac_id, "CBF_radius", col_rad)
            sender.send_setting(ac_id, "CBF_gamma", gamma)
            sender.send_block(ac_id, block_id)

            sender.send_setting(ac_id, "sr_speed", speed)
            sender.send_setting(ac_id, "kp", kp)
            #sender.send_setting(1, "Gain", 1)
            #sender.send_setting(1, "Radius", 5)
            sleep(1)

        sender.stop()
    else:
        print("Please, introduce at least one ac_id.")

