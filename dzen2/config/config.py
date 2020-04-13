#!/bin/python

def __init__():
	pass

#________________________________________________________________________________
# FONT:

# The following -terminal- font should work on any system, but
# it's not monospaced, therefore bar positioning is messy with it
# FONT = "*-terminal-medium-*-*-14-*-*-*-*-*-*-*"

# This one gives nicely aligned bar, but it won't work by default.
# Read how toget it work: https://github.com/Ermiq/dzen2-bar2/edit/master/README.md
FONT = "-*-liberation mono-*-*-*-*-14-*-*-*-m-*-*-*"


# Widgets list:
'''The format is:
[
"RAMWidget"		- widget name (file name without *.py)
30				- Max characters in output text
"1, nautilus"	- mouse button, command to execute on mouse button
]
'''
WIDGETS = [
	[ "MediaplayerWidget",	40,	"1, rhythmbox"		],
	[ "WiFiWidget",			18,	"1, wicd-client"	],
	[ "RAMWidget",			30,	"1, nautilus"		],
    [ "BatteryWidget",		30	],
	[ "VolumeWidget",		7	],
	[ "DateWidget",			20	],
]

# Some colors:
clrTX1 = '#DBDADA'		# medium grey text
clrTX2 = '#F9F9F9'		# light grey text
clrGRY = '#909090'		# dark grey text
clrOFF = '#444444'		# very dark gray (WiFi off)

clrBAR = '#A6F09D'		# light green of bar-graphs
clrGRN = '#65A765'		# dark green of bar-graphs
clrBGR = '#00FF00'		# clear bright green

clrYEL = '#FFF600'		# light yellow (caution)
clrORG = '#FFAE00'		# dark orange
clrRED = '#FF0000'		# red (warning)

clrWHT = '#FFFFFF'		# default bar foreground (white)
clrBLK = '#000000'		# black


# Bar size:
BAR_WIDTH = '1920'
BAR_HEIGHT = '50'	# doesn't change anything... Have no idea.)))

# Default width limit for widget content:
DEFAULT_WIDGET_WIDTH = 10	# Characters amount, not pixels!

# Separator:
# Looks like a green vertical line 2 pixels width,
# 8 pxls empty space before the sep and 8 pxls empty after it.
SEP = "^p(8;)^fg(" + clrGRN + ")^r(2x" + BAR_HEIGHT + ")^p(8;)^fg(" + \
	clrWHT + ")"


# Update interval:
SLEEP = 1       # whole seconds, no decimals!


# Workspaces header:
WORKSPACE_HEADER = " "


# Date/time format:
DATE_FORMAT = "%a, %d %b. %H:%M:%S"


# WiFi widget header:
WIFI_HEADER = "WiFi:"
# Name of WiFi interface (see your '/sbin/iwconfig' output). Could be "wlan0" on some distros):
WIFI_INTERFACE = "wlp2s0"


# Volume widget:
VOLUME_HEADER = "VOL:"


# RAM widget:
RAM_HEADER = "RAM:"


# Battery widget:
BATTERY_HEADER = "BAT:"


# Mediaplayer widget settings:
# Show the playing track as "Song name - Artist" or "Artist - Song name"
SONG_FIRST = True
# Widget will check if one of these players is running,
# the first match will be used as a source for widget output:
PLAYERS = [ "rhythmbox", "audacious", "spotify", "vlc", "quodlibet", "xmms2", "mplayer" ]