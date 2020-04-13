#!/bin/python

import sys
import subprocess
import time  # for sleep()
from traceback import format_exc
from helpers import shellHelper

import widgets.date
import widgets.battery
import widgets.memory
import widgets.volume
import widgets.wifi
import widgets.mediaplayer
import widgets.i3workspacesparser

from config import config
import json

global I3_WIDGET
global WIDGETS
global HEADER
global OFFSET
global OUTPUT

def __init__():
	'''To get access to stuff in this file.'''
	pass

# Useful functions:
# ------------------------------------------------------------------------------------

def KillProcess(processName, leaveNumInstancesAlive=1):
	"Kill currently running processes with the given name, and leave alive just the given amount of instances."
	output = shellHelper.ExecOneLine(
		"pgrep " + processName + " | awk '{print $1}'")

	instances = output.split()

	for i in range(len(instances) - leaveNumInstancesAlive):
		shellHelper.ExecOneLine("kill -9 " + instances[i])
	return

# To kill all additional dzen2 instances currently running:
# KillProcess("dzen2", 1)


# Main:
# -------------------------------------------------------------------------------

def Start():
	global I3_WIDGET, WIDGETS, HEADER
	# Declare the i3 compatible special snowflake widget.
	I3_WIDGET = widgets.i3workspacesparser.i3WorkspacesWidget(100, "1, rhythmbox")

	# Declare other ordinary widgets:
	WIDGETS = [
		widgets.mediaplayer.MediaPlayerWidget(50, "1, rhythmbox"),
		widgets.wifi.WiFiWidget(25, "1, wicd-client"),
		widgets.memory.MemoryWidget(30, "1, nautilus"),
		widgets.battery.BatteryWidget(22),
		widgets.volume.VolumeWidget(7),
		widgets.date.DateWidget(22)
	]

def Loop():
	global I3_WIDGET, WIDGETS, HEADER, OFFSET, OUTPUT
	# HEADER for dzen2 line. Sets default font, foreground color, draws a colored frame that outlines the bar.
	# The "^pa(0;0)" at the end of HEADER tells dzen2 to draw things from the
	# beginning of the bar and at the very top of the screen.
	# It will make text seem to go too mich high, but at the same time
	# it makes widgets clickable even if mouse cursor is pointing at the top
	# edge of the screen.
	# If move text a bit lower, will have to aim at the very widget text to clickon it,
	# otherwise, at the edge of the screen, clicks are not registered, they only
	# work on text itself.
	HEADER = "^fn(" + config.FONT + ")" + "^ib(1)^pa(0;0)^fg(" + config.clrBAR + ")^ro(" + \
		config.BAR_WIDTH + "x" + config.BAR_HEIGHT + ")^pa(0;0)"
	
	I3_WIDGET.Update()
	# i3 widget returns a list of workspaces.
	for workspace in I3_WIDGET.Dzen():
		HEADER += workspace

	# OUTPUT collects the overall line generated that will be piped to dzen2.
	# Very first bar element after the header (besides the special snowflake i3 widget)
	# is a separator:
	OUTPUT = config.SEP

	# The OFFSET will go to the result dzen2 stream line right after the HEADER,
	# so widgets contents data will start from the position that is determined by SCREEN_WIDTH and OFFSET.
	# E.g.:
	# screen size is 1920, widgets content takes 800 pxls,
	# so, first widget should start at 1120 pxls from 0;0 (the left top corner of the screen).
	# OFFSET counts how many pixels wide the overall widgets content is.
	# to make it possible to align the bar at the right side more or less properly).
	# First value in OFFSET is a separator SEP (has been just added above) which is
	# 18 pixels wide.
	OFFSET = 18

	for i in WIDGETS:
		i.Update()				# Update widget data.
		i.WIDTH_PXL = OFFSET	# Could be used to get X coordinate of the widget.
		OUTPUT += i.Dzen()		# Add widget dzen2 content to OUTPUT.
		OUTPUT += config.SEP	# Separator after every widget.
		OFFSET += i.WidthPxl(config.FONT)	# Count the width in pixels. Calculated using 'dzen2-textwidth' tool.
		OFFSET += 18			# Separator after every widget

	# How many pixels the line should be moved on to the right
	OFFSET = int(config.BAR_WIDTH) - int(OFFSET)

	# Convert OFFSET into dzen2 abra-cadabra:
	OFFSET = "^pa(" + str(OFFSET) + ";0)"
	# This (0;0) option could be used instead to simply start widgets on the left side:
#	OFFSET = "^pa(0;0)"
	# But it will ignore the i3 workspace widget. Didn't work on it yet.

	# The final line build:
	OUTPUT = HEADER + OFFSET + OUTPUT

	return OUTPUT

if __name__ == "__main__":	
	Start()

	while  True:
		try:
			Loop()
		except subprocess.CalledProcessError as e:
			if e.output.startswith('error'):
				error = json.loads(e.output[7:]) # Skip "error: "
				OUTPUT = error['message']
		except FileNotFoundError as e:
			OUTPUT = e.strerror
		# Send the generated dzen2 abra-cadabra-line (or an error?)
		# to standard output.
		# In 'dzen2-startup.sh' script it will be piped to dzen2.
		sys.stdout.write(OUTPUT + "\n")
		sys.stdout.flush()

		time.sleep(config.SLEEP)