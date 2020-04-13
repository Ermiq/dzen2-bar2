#!/bin/python

import re
from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class WiFiWidget(WidgetBase):
	IS_UP = False
	CONNECTED = False
	QUALITY = 0
	ESSID = ""

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = config.WIFI_HEADER

	def Update(self):
		# Get iwconfig report:
		output = shellHelper.ExecOneLine("/sbin/iwconfig " + config.WIFI_INTERFACE)
		# Check if WiFi adapter is turned on: "Tx-Power=22 dBm" or "Tx-Power=off"
		POWER_STATE = re.search('%s(.*)%s' % ("Tx-Power=", " "), output).group(1)

		if POWER_STATE != "off":
			IS_UP = True
			# Check connection status:
			if shellHelper.ExecOneLine("cat /sys/class/net/" + config.WIFI_INTERFACE + "/operstate") != 'down':
				self.CONNECTED = True

		if IS_UP:
			if self.CONNECTED:
				# Connected to some SSID:
				self.ESSID = re.search('%s(.*)%s' % ('ESSID:"', '"'), output).group(1)
				self.QUALITY = self.GetQualityLevel()
				output = self.ESSID + "(" + str(self.QUALITY) + "%)"
			else:
				# WiFi is on but not connected to any SSID:
				output = "No connection"
		else:
			# Wifi adapter is off:
			output = "Off"
		self.TEXT = output

	def Dzen(self):
		# Color depends on connection quality:
		if self.QUALITY > 80:
			self.TEXT_COLOR = config.clrBGR
		elif self.QUALITY == 0:
			self.TEXT_COLOR = config.clrOFF
		elif self.QUALITY < 40:
			self.TEXT_COLOR = config.clrRED
		elif self.QUALITY < 60:
			self.TEXT_COLOR = config.clrORG
		elif self.QUALITY < 80:
			self.TEXT_COLOR = config.clrYEL
		self.TextFormat()
		self.DZEN2LINE = self.HEADER + "^fg(" + self.TEXT_COLOR + ")" + self.TEXT
		self.AddAction()
		return self.DZEN2LINE

	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font)
		return w

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
				if re.search(config.WIFI_INTERFACE + ':', line):
					# Found line with values. Split it into a list of entries:
					line = line.split()
					# Get digital value from the 3rd entry (index 2 in list).
					# r'|d+' represents a regular expression for digits:
					line = re.search(r'\d+', line[2]).group(0)
					# 70 in the table means 100%, so gotta change the value to real percentage:
					return int(int(line) * 100 / 70)