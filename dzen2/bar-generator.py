#!/bin/python

import sys
import subprocess
import time  # for sleep()
import widgets.date
import widgets.battery
import widgets.memory
import widgets.volume
import widgets.wifi
import widgets.i3workspacesparser

# FONT="bitstream-terminal-bold-r-normal--5-14-10-10-c-11-iso8859-1"
FONT = "-*-lucidatypewriter-bold-*-*-*-14-100-*-*-*-*-*-*"
BAR_WIDTH = '1920'
BAR_HEIGHT = '16'

# Define colors and spacers etc..:
TX1 = '#DBDADA'     # medium grey text
TX2 = '#F9F9F9'     # light grey text
GRY = '#909090'     # dark grey text
BAR = '#A6F09D'     # green background of bar-graphs
GRN = '#65A765'     # light green (normal)
YEL = '#FFFFBF'     # light yellow (caution)
RED = '#FF0000'     # light red/pink (warning)
WHT = '#FFFFFF'     # white
BLK = '#000000'     # black
SEP = "^p(8;)^fg(" + GRN + ")^r(2x" + BAR_HEIGHT + ")^p(8;)^fg(" + \
	WHT + ")"  # item separator block/line
SLEEP = 1           # update interval (whole seconds, no decimals!)
CHAR = 20      # pixel width of characters of font used

# ------------------------------------------------------------------------------------


def KillProcess(processName, leaveNumInstancesAlive=1):
	"Kill currently running processes with the given name, and leave alive just the given amount of instances."
	output = subprocess.check_output(
		"pgrep " + processName + " | awk '{print $1}'", shell=True, universal_newlines=True)

	instances = output.split()

	for i in range(len(instances) - leaveNumInstancesAlive):
		subprocess.call("kill -9 " + instances[i], shell=True)
	return


def GetFromShell(processStr):
	out = subprocess.check_output(
		processStr, shell=True, universal_newlines=True).strip()
	return out

# -------------------------------------------------------------------------------

# Kill all additional dzen2 instances currently running:
#KillProcess("dzen2", 1)

def Start():
	# Declare i3 compatible special snowflake widget.
	i3Widget = widgets.i3workspacesparser.i3WorkspacesWidget(100)

	# Declare other ordinary widgets:
	WIDGETS = [
		widgets.wifi.WiFiWidget(25),
		widgets.volume.VolumeWidget(3),
		widgets.memory.MemoryWidget(30),
		widgets.battery.BatteryWidget(22),
		widgets.date.DateWidget(22)
	]

	while True:
		# HEADER for dzen2 line. Sets default font, foreground color, draws a colored frame that outlines the bar.
		HEADER = "^fn(" + FONT + ")" + "^ib(1)^pa(0;0)^fg(" + BAR + ")^ro(" + \
			BAR_WIDTH + "x" + BAR_HEIGHT + ")^pa(0;0)"

		# The widget returns a list of workspaces data.
		i3Widget.Update()
		for workspace in i3Widget.Dzen():
			HEADER += workspace
		
		# OUTPUT collects the overall line generated that will be piped to dzen2.
		# Very first bar element after the header (besides the special snowflake i3 widget)
		# - a separator:
		OUTPUT = SEP
		# OFFSET counts how many pixels wide the overall bar content is.
		# to make it possible to align the bar at the right side more or less properly).
		# Separators are 18 pxl wide.
		OFFSET = 18
		for i in WIDGETS:
			i.Update()					# Update widget data.
			OUTPUT += i.Dzen()			# Add widget dzen2 content to OUTPUT.
			OUTPUT += SEP				# Separator after every widget.
			OFFSET += i.WidthPxl(FONT)	# Count the width in pixels. Every widget counts it with 'dzen2-textwidth' tool.
			OFFSET += 18				# Separator after every widget
		# Last separator at the end of the line.
		OFFSET += 18

		# Calculate how much the line should be moved to the right
		OFFSET = int(BAR_WIDTH) - int(OFFSET)
		# This line will go right after the HEADER, so widgets contents data will start
		# from the position that is determined by this calculations. E.g.,
		# screen size is 1920, widgets content takes 800 pxls,
		# so, first widget should start at 1120 pxls from 0;0 (the left top corner of the screen).
		OFFSET = "^pa(" + str(OFFSET) + ";0)"
		# This (0;0) option could be used instead to start widgets on the left side
#		OFFSET = "^pa(0;0)"

		OUTPUT = HEADER + OFFSET + OUTPUT

		# Send the generated dzen2 abra-cadabra-line to standard output.
		sys.stdout.write(OUTPUT + "\n")
		sys.stdout.flush()
		# Take a rest for a second.
		time.sleep(SLEEP)

if __name__ == "__main__":
	Start()
	pass