#!/bin/python

import re
from .widgetBase import Widget

class WiFiWidget(Widget):

	INTERFACE = "wlp2s0"
	IS_UP = False
	CONNECTED = False
	QUALITY = 0
	ESSID = ""

	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "WiFi: "

	def Update(self):
		# Get iwconfig report:
		output = self.GetFromShell("/sbin/iwconfig " + self.INTERFACE)
		# Check if WiFi adapter is turned on: "Tx-Power=22 dBm" or "Tx-Power=off"
		POWER_STATE = re.search('%s(.*)%s' % ("Tx-Power=", " "), output).group(1)

		if POWER_STATE != "off":
			IS_UP = True
			# Check connection status:
			if self.GetFromShell("cat /sys/class/net/" + self.INTERFACE + "/operstate") != 'down':
				CONNECTED = True

		if IS_UP:
			if CONNECTED:
				# Connected to some SSID:
				ESSID = re.search('%s(.*)%s' % ('ESSID:"', '"'), output).group(1)
				self.QUALITY = self.GetQualityLevel()
				output = ESSID + "(" + str(self.QUALITY) + "%)"
			else:
				# WiFi is on but not connected to any SSID:
				output = "No connection"
		else:
			# Wifi is off:
			output = "Off"
		self.TEXT = output
		self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)

	def Dzen(self):
		# Color depends on connection quality:
		if self.QUALITY > 80:
			color = "#00FF00"
		elif self.QUALITY == 0:
			color = "#444444"
		elif self.QUALITY < 40:
			color = "#FF0000"
		elif self.QUALITY < 60:
			color = "#FFAE00"
		elif self.QUALITY < 80:
			color = "#FFF600"

		return self.HEADER + "^fg(" + color + ")" + self.TEXT

	def Width(self):
		return self.WIDTH

	def WidthPxl(self, font):
		w = self.GetFromShell("dzen2-textwidth " + font + " '" + self.HEADER + self.TEXT + "'")
		return int(w)

	def GetQualityLevel(self):
		'''cat /proc/net/wireless returns this kind of data:

Inter-| sta-|      Quality     |     Discarded packets      | Missed | WE
 face | tus | link level noise | nwid crypt frag retry misc | beacon | 22
wlp2s0: 0000   70.  -39.  -256     0      0      0      0       61      0

To determine connection quality level (0-100%) need to extract the "Qualuty -> link" entry from 
he table. When this entry = 70. it means the connection quality is 100% stable.
		'''
		with open("/proc/net/wireless") as origin_file:
			# Iterate through lines:
			for line in origin_file:
				# Look for "wlp2s0:" or "wlan0:" in lines:
				if re.search(self.INTERFACE + ':', line):
					# Found line with values. Split it into a list of entries:
					line = line.split()
					# Get digital value from the 3rd entry (index 2 in list).
					# r'|d+' represents a regular expression for digits:
					line = re.search(r'\d+', line[2]).group(0)
					# 70 in the table means 100%, so gotta change the value to real percentage:
					return int(int(line) * 100 / 70)