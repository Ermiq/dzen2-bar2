#!/bin/python

import sys
import subprocess
import time  # for sleep()
import importlib
from traceback import format_exc
from helpers import shellHelper

from config import config
import json

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

def Initialize():
	'''Initialize widgets.'''
	global WORKSPACE_WIDGET, WIDGETS, HEADER, OFFSET, OUTPUT

	# Try to load i3 widget module (from file i3workspaceparser):
	try:
		from widgets.i3workspacesparser import i3WorkspacesWidget
		WORKSPACE_WIDGET = i3WorkspacesWidget(20)
	except:
		WORKSPACE_WIDGET = None
		pass
	
	# Get other widgets from a list in config module.
	'''In config, widgets are described as a list of properties:
	1 - widget class name (should be the same as file name without "*.py");
	2 - widget width: will be set to default if not provided;
	3 - mouse action: for example: "1, firefox". Will be ""(none)
	if not provided.'''
	WIDGETS = []
	for description in config.WIDGETS:
		name	= description[0]
		width	= description[1] if len(description) > 1 else config.DEFAULT_WIDGET_WIDTH
		action	= description[2] if len(description) > 2 else ""
		
		_module	= importlib.import_module("widgets." + name)
		_class	= getattr(_module, name)
		_instance = _class(width, action)
		WIDGETS.append(_instance)
	pass

def Loop():
	global WORKSPACE_WIDGET, WIDGETS, HEADER, OFFSET, OUTPUT
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
	
	if WORKSPACE_WIDGET:
		# i3 widget returns a list of workspaces.
		WORKSPACE_WIDGET.Update()
		for workspace in WORKSPACE_WIDGET.Dzen():
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

	# Update widget data:
	for i in WIDGETS:
		i.Update()
		i.WIDTH_PXL = OFFSET	# Could be used to get X coordinate of the widget.
		OUTPUT += i.Dzen()		# Send widget dzen2 content to OUTPUT.
		OUTPUT += config.SEP	# Separator after every widget.
		OFFSET += i.WidthPxl(config.FONT)	# Count the width in pixels. Calculated using 'dzen2-textwidth' tool.
		OFFSET += 18			# Width of separator after every widget

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
	Initialize()

	while  True:
		try:
			Loop()
		# Workaround for errors, if occured:
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