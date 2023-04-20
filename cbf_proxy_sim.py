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
Script to generate an easy call for pprzlink_proxy.
'''

import os
from time import sleep

PAPARAZZI_HOME = os.getenv("PAPARAZZI_HOME")

PAPARAZZI_PROXY = PAPARAZZI_HOME + "/sw/ground_segment/tmtc/pprzlink_proxy.py"
AIRFRAME_DIR = "airframes/UGR/"
AIRFRAME_DIR_LONG = PAPARAZZI_HOME + "/conf/" + AIRFRAME_DIR

INIT_OUT_PORT = 4244
INIT_IN_PORT = 4245
INIT_AC_ID = 1 # should be more than 0 and less than 255

NUM_AGENTS = 3

# -------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description="Circular formation")
	parser.add_argument('-v', '--v', dest='verbose', action='store_true', help="Pprz_proxy verbose argument")
	args = parser.parse_args()

	verbose = args.verbose

	# Generate the pprzlink_proxy args
	pprz_proxy_args = " "
	for n in range(NUM_AGENTS):
		ac_id = INIT_AC_ID + n
		out_port = INIT_OUT_PORT + 2*n
		in_port = INIT_IN_PORT + 2*n

		pprz_proxy_args += "--ac=" + str(ac_id) + ":" + str(out_port) + ":" + str(in_port) + " "

	sleep(1)

	try:
		# Execute pprzlink_proxy with the generated args
		print(" ------------------------ ")
		print("Custom pprzlink_proxy arguments:\n\t" + pprz_proxy_args + "\n")
		if verbose:
			os.system("python3 " + PAPARAZZI_PROXY + pprz_proxy_args + "-v")
		else:
			os.system("python3 " + PAPARAZZI_PROXY + pprz_proxy_args)

	except (KeyboardInterrupt, SystemExit):
		pass
		
		

	
	
	


		


		
	

    
