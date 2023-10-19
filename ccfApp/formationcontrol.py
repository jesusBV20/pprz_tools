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

import numpy as np
from time import sleep

from PySide6.QtCore import QObject, Signal

def wrap(x):
    return (x)
class FormationControlWorker(QObject):

    progress = Signal()
    finished = Signal()

    def __init__(self, conf, log_reporter):
        super().__init__()
        self.conf = conf
        self.log_reporter = log_reporter

    def run(self):
        while self.conf.ccfstate:
            self.circular_formation()
            self.progress.emit()
            sleep(1) #TODO: better freq control
        self.log_reporter.log("INFO: CCF thread stopped -")
        self.finished.emit()

    '''\
    Circular Formation Control algorithm
    '''
    def circular_formation(self):
        ac_info_list = self.conf.ac_info_list
        delta_info_list = self.conf.delta_info_list
        self.conf.sigma_list = np.zeros(len(self.conf.ac_info_list))

        # Compute the inter-vehicle errors
        i = 0
        for ac_info in ac_info_list:
            ac = ac_info.ac

            # Compute the inter-vehicle errors
            ac.sigma = np.arctan2(ac.XY[1]-ac.XYc[1], ac.XY[0]-ac.XYc[0])
            self.conf.sigma_list[i] = ac.sigma

            i = i + 1

        # Build delta_desired vector
        delta_desired = np.zeros(len(delta_info_list))
        
        i = 0
        for delta_info in delta_info_list:
            delta_desired[i] = delta_info.value * np.pi/180

            i = i + 1

        inter_sigma = self.conf.B.transpose().dot(self.conf.sigma_list)
        error_sigma = inter_sigma - delta_desired

        if np.size(error_sigma) > 1:
            for i in range(0, np.size(error_sigma)):
                if error_sigma[i] > np.pi:
                    error_sigma[i] = error_sigma[i] - 2*np.pi
                elif error_sigma[i] <= -np.pi:
                    error_sigma[i] = error_sigma[i] + 2*np.pi
        else:
            if error_sigma > np.pi:
                error_sigma = error_sigma - 2*np.pi
            elif error_sigma <= -np.pi:
                error_sigma = error_sigma + 2*np.pi

        u = - ac_info_list[0].ac.s * self.conf.k *  self.conf.B.dot(error_sigma)
        self.conf.u_list = np.clip(u, -self.conf.u_max, self.conf.u_max)

        # SEND RADIUS SETTING MSGs
