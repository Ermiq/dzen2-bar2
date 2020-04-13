#!/bin/python

import re
from widgets.WidgetBase.WidgetBase import WidgetBase
from helpers import shellHelper
from config import config

class BatteryWidget(WidgetBase):

	LEVEL = 0
	STATUS = ""
	INDICATOR_LENGTH = 50
	GRAPHICAL = True
	
	# Not used:
	SHOW_ARROW = False  # Looks ugly, and block change the size
	WAS_ARROW = True	# To switch arrow on/off
	
	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = config.BATTERY_HEADER

	def Update(self):
		'''
		'acpi -b' returns something like: "Battery 0: Charging, 94%".
		For some reason the charging status sometimes returned as "Unknown".
		In this case we'll check AC adapter connectivity state with 
		'acpi -a'. It will give "Adapter 0: on-line" or "off-line".
		'''
		acpi_report = shellHelper.ExecOneLine("acpi -b")
		self.LEVEL = re.findall(r'\d+', acpi_report)[1]
		self.STATUS = re.search(
			'%s(.*)%s' % ("Battery "r'\d+'": ", ", "), acpi_report).group(1)

		if self.STATUS == "Unknown":
			AC = shellHelper.ExecOneLine("acpi -a | grep -oP '(?<=: ).*'")
			if AC == "on-line":
				self.STATUS = "Charging"
			elif AC == "off-line":
				self.STATUS = "Discharging"

		'''
		if STATUS == "Charging":
			STATUS = 
		elif STATUS == "Discharging":
			if BAT < 50:
				STATUS = 
			elif BAT < 25:
				STATUS = 
			else STATUS = 
		'''

		# Set urgent flag below 5% or use orange below 20%
		if int(self.LEVEL) < 5:
			config.clrRED
		elif int(self.LEVEL) < 20:
			config.clrORG
		else:
			config.clrWHT

		if not self.GRAPHICAL:
			self.TEXT = self.LEVEL + "%, " + self.STATUS

	def Dzen(self):
		if self.GRAPHICAL:
			self.DZEN2LINE = self.HEADER + self.GetGraphicalBar()
		else:
			self.TextFormat()
			self.DZEN2LINE = self.HEADER + "^fg(" + self.TEXT_COLOR + ")" + self.TEXT
		self.AddAction()
		return self.DZEN2LINE

	def WidthPxl(self, font):
		if self.GRAPHICAL:
			w = WidgetBase.WidthPxl(self, font) + self.INDICATOR_LENGTH
		else:
			w = WidgetBase.WidthPxl(self, font)
		return w

	def GetGraphicalBar(self):
		drainbar = int((100 - int(self.LEVEL)) * (self.INDICATOR_LENGTH / 100))
		leftbar = int(int(self.LEVEL) * (self.INDICATOR_LENGTH / 100))

		if int(self.LEVEL) <= 20:
			fgcol = config.clrRED
		else:
			fgcol = config.clrGRN

		'''
		# Here lies an ugly arrow indicator for battery.
		You can try it by replacing the last 'return' part with this commented stuff:

		if self.STATUS == "Charging":
			arrow = ">>"
		else:
			arrow = "<<"
		if self.WAS_ARROW:
			self.WAS_ARROW = False
			result = "^fg(white)^p(;4)" + fgcol + "^r(" + str(leftbar) + \
				"x8)^fg(" + self.BAR + ")^r(" + \
				str(drawnbar) + "x8)^p(;-4)"
		else:
			self.WAS_ARROW = True
			result = "^fg(white)^p(;4)" + fgcol + "^ro(" + str(leftbar) + \
				"x8)^fg(" + self.BAR + ")^ro(" + str(drawnbar) + "x8)^p(;-4)^p(-" + str(
					self.INDICATOR_LENGTH / 2) + ";)" + arrow + " ^p(" + str(self.INDICATOR_LENGTH / 2) + ";)"
		'''
		result = "^fg(white)^p(;4)^fg(" + config.clrBGR + ")^r(" + str(leftbar) + \
				"x8)^fg(" + fgcol + ")^r(" + \
				str(drainbar) + "x8)^p(;-4)"
		return result
