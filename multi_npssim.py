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
Building in progress python script to autogenerate the simulation of n agents.
'''
import os
import sys
import subprocess
from time import sleep

from math import floor
from re import search

PAPARAZZI_HOME = os.getenv("PAPARAZZI_HOME")

PAPARAZZI_PROXY = PAPARAZZI_HOME + "/sw/ground_segment/tmtc/pprzlink_proxy.py"
USERCONFIG_DIR = PAPARAZZI_HOME + "/conf/userconf/GVF/"
AIRFRAME_DIR = "airframes/UGR/"
AIRFRAME_DIR_LONG = PAPARAZZI_HOME + "/conf/" + AIRFRAME_DIR
AIRFRAME_FILE  = "gvf_cbf_steering_rover.xml"

AIRFRAME_NAME = "gvf_rover"
CONF_RADIO = "radios/UCM/T16SZ_SBUS_rover.xml"
CONF_TELEMETRY = "telemetry/GVF/gvf_multi_rover.xml"
CONF_FLIGHTPLAN = "flight_plans/UGR/multi/multi_steering_rover_gvfMission.xml"
CONF_SETTINGS = ""
CONF_MODULES = ""
CONF_COLOR = ""

INIT_OUT_PORT = 4244
INIT_IN_PORT = 4245
INIT_AC_ID = 1 # should be more than 0 and less than 255

NUM_AGENTS = 3

GUI_COLORS = ["blue", "red", "green", "purple", "orange", "white", "black"]

# Generate the airframe file ----------------------------------------------------------------------------------------------------
def gen_airframe(airframe_file, ac_id , out_port, in_port):
	out_port = str(out_port)
	in_port = str(in_port)
	ac_id = str(ac_id)

	for i, line in enumerate(airframe_file):
		if search("MODEM_PORT_OUT", line):
			modem_init_line = i
			break
	
	airframe_file[0] = "<!DOCTYPE airframe SYSTEM \"../../airframe.dtd\">"
	airframe_file[modem_init_line] = "      <configure name=\"MODEM_PORT_OUT\" value=\"" + out_port + "\"/>\n"
	airframe_file[modem_init_line + 1] = "      <configure name=\"MODEM_PORT_IN\" value=\"" + in_port + "\"/>\n"

	file_name = AIRFRAME_FILE.replace(".xml", "_n" + ac_id + ".xml")

	with open(AIRFRAME_DIR_LONG + "multi/" + file_name, "w") as f:
		f.writelines(airframe_file)
		print("File generated: " + AIRFRAME_DIR_LONG + "multi/" + file_name)
# -------------------------------------------------------------------------------------------------------------------------------

# Generate the aricraft user configuration --------------------------------------------------------------------------------------
def gen_aircraftconfig(ac_id, num_agent):
	if (CONF_COLOR == ""):
		color_id = num_agent - floor((num_agent + 1)/len(GUI_COLORS)) * len(GUI_COLORS)
		color = GUI_COLORS[color_id]
	else:
		color = CONF_COLOR

	ac_id = str(ac_id)
	file_name = AIRFRAME_FILE.replace(".xml", "_n" + ac_id + ".xml")
	
	aircraft_conf = "  <aircraft\n"
	aircraft_conf += "   name=\"" + AIRFRAME_NAME + "_n" + ac_id + "\"\n"
	aircraft_conf += "   ac_id=\"" + ac_id + "\"\n"
	aircraft_conf += "   airframe=\"" + AIRFRAME_DIR + "multi/" + file_name + "\"\n"
	aircraft_conf += "   radio=\"" + CONF_RADIO + "\"\n"
	aircraft_conf += "   telemetry=\"" + CONF_TELEMETRY + "\"\n"
	aircraft_conf += "   flight_plan=\"" + CONF_FLIGHTPLAN + "\"\n"
	aircraft_conf += "   settings=\"" + CONF_SETTINGS + "\"\n"
	aircraft_conf += "   settings_modules=\"" + CONF_MODULES + "\"\n"
	aircraft_conf += "   gui_color=\"" + color + "\"\n"
	aircraft_conf += "  />\n"
	return aircraft_conf
# -------------------------------------------------------------------------------------------------------------------------------

# Generate the control panel configuration (Session with pre-defined simulations) -----------------------------------------------
def gen_controlpanel(aircraft_names):
	sim_lines = [None, None]
	
	sim_sesionconfig = ""
	for ac in aircraft_names:
		sim_sesionconfig += "      <program name=\"Simulator\">\n"
		sim_sesionconfig += "      	<arg flag=\"-a\" constant=\"" + ac + "\"/>\n"
		sim_sesionconfig += "      </program>\n"
	
	with open(USERCONFIG_DIR + "gvf_control_panel.xml", "r") as f:
		panel_lines = f.readlines()
		for i, line in enumerate(panel_lines):
			if search("simulations-begin", line):
				sim_lines[0] = i	
			if search("simulations-end", line):
				sim_lines[1] = i
				break
			
	if sim_lines[0] != None and sim_lines[1] != None:
		try:
			with open(USERCONFIG_DIR + "writing-gvf_control_panel.xml", "w") as f:
				for i in range(len(panel_lines)):
					if i <= sim_lines[0] or i >= sim_lines[1]:
						f.write(panel_lines[i])
					if i == sim_lines[0]:
						f.write(sim_sesionconfig)
			
			os.system("cp " + USERCONFIG_DIR + "writing-gvf_control_panel.xml " + USERCONFIG_DIR + "gvf_control_panel.xml")
			os.system("rm " + USERCONFIG_DIR + "writing-gvf_control_panel.xml")	
			print("File edited: " + USERCONFIG_DIR + "gvf_control_panel.xml")
		except:
			os.system("rm " + USERCONFIG_DIR + "writing-gvf_control_panel.xml")					
# -------------------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
	import argparse
	
	parser = argparse.ArgumentParser(description="Multiple agents nps_sim generator")
	parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', help="show msg tracking from pprzlink_proxy")
	parser.add_argument('-t', '--test', dest='test', action='store_true', help="test the generated AC configurations")
	parser.add_argument('-p', '--proxy', dest='proxy', action='store_true', help="launch pprzlink_proxy")
	verbose = parser.parse_args().verbose
	proxy = parser.parse_args().proxy
	test = parser.parse_args().test

	# Read the original airframe file
	with open(AIRFRAME_DIR_LONG + AIRFRAME_FILE, "r") as f:
		airframe_file = f.readlines()
	
	# Generate the new airframe files directory (or clean it)
	try:
		os.mkdir(AIRFRAME_DIR_LONG + "multi")
	except:
		try:
			os.system("rm -v " + AIRFRAME_DIR_LONG + "multi/" + "*")
		except:
			pass
	
	# Generate the airframe files, aircraft configs and pprzlink_proxy args
	pprz_proxy_args = " "
	aircraft_names = []
	userconfig_file = "<conf>\n"
	for n in range(NUM_AGENTS):
		ac_id = INIT_AC_ID + n
		out_port = INIT_OUT_PORT + 2*n
		in_port = INIT_IN_PORT + 2*n

		gen_airframe(airframe_file, ac_id, out_port, in_port)
		userconfig_file += gen_aircraftconfig(ac_id, n)
		pprz_proxy_args += "--ac=" + str(ac_id) + ":" + str(out_port) + ":" + str(in_port) + " "
		aircraft_names.append(AIRFRAME_NAME + "_n" + str(ac_id))

	userconfig_file += "</conf>\n"

	# Generate the userconfig file (load it with paparazzi/start.py)
	with open(USERCONFIG_DIR + "gvf_multi_conf.xml", "w") as f:
		f.write(userconfig_file)
		print("File generated: " + USERCONFIG_DIR + "gvf_multi_conf.xml")

	# Generate the user panel configuration
	gen_controlpanel(aircraft_names)

	sleep(1)
	process_queue = []
	try:
		# Test the generated configurations
		if test:
			print(" ------------------------ ")
			os.system("make test_gvf_multi -C " + PAPARAZZI_HOME)
		
		# Execute pprzlink_proxy with the generated args
		if proxy:
			print(" ------------------------ ")
			print("Custom pprzlink_proxy arguments:\n\t" + pprz_proxy_args + "\n")
			if verbose:
				os.system("python2 " + PAPARAZZI_PROXY + pprz_proxy_args + "-v")
			else:
				os.system("python2 " + PAPARAZZI_PROXY + pprz_proxy_args)

	except (KeyboardInterrupt, SystemExit):
		pass
		
		

	
	
	


		


		
	

    
