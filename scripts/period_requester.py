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

DEFAULT_ADDRESS = "127.0.0.1"

# GCS ID, OUT port, IN port
gcs_conf = [0, DEFAULT_ADDRESS, 4243, 4242]

class sender:
    def __init__(self, ac_id) -> None:
        self.ac_id = ac_id
        self.interface = IvyMessagesInterface("Periodic DL_VALUE requester")

    def get_dl_value(self):
        msg = PprzMessage("ground", "GET_DL_SETTING")
        msg['ac_id'] = self.ac_id
        msg["index"] = 0
        self.interface.send(msg)

    def stop(self):
        # Stop IVY interface
        if self.interface is not None:
            self.interface.shutdown()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Periodic DL_VALUE requester")
    parser.add_argument('-ac_id', '--ac_id', dest='ac_id', type=str, default=None, help="ID of the receiver AC")
    parser.add_argument('-f', '--f', dest='freq', type=float, default=0.1, help="DL_VALUE request frequency (time in seconds between messages)")

    # ---
    args = parser.parse_args()
    
    # Script parameters and setting
    ac_id = args.ac_id
    freq = args.freq
    # ---
    
    if ac_id is not None:
        ac_sender = sender(ac_id)

        try:
            while (True):
                ac_sender.get_dl_value()
                sleep(freq)

        except (KeyboardInterrupt):
            ac_sender.stop()
            print("\n- Script killed by Keyboard Interruption-")

    else:
        print("- Please, introduce an ac_id -")

