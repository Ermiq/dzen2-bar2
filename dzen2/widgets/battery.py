#!/bin/python

import re
from .widgetBase import Widget


class BatteryWidget(Widget):

	LEVEL = 0
	STATUS = ""
	INDICATOR_LENGTH = 50
	GRAPHICAL = True
	BAR = '#A6F09D'     # green background of bar-graphs
	GRN = '#65A765'     # light green (normal)
	RED = '#FF0000'     # light red/pink (warning)
	
	# Not used by default:
	SHOW_ARROW = False  # Looks ugly, and block changes the size
	WAS_ARROW = True	# To switch arrow on/off
	
	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "BAT: "

	def Update(self):
		'''
		'acpi -b' returns something like: "Battery 0: Charging, 94%".
		For some reason the charging status sometimes returned as "Unknown".
		In this case we'll check AC adapter connectivity state with 
		'acpi -a'. It will give "Adapter 0: on-line" or "off-line".
		'''
		acpi_report = self.GetFromShell(["acpi", "-b"])
		self.LEVEL = re.findall(r'\d+', acpi_report)[1]
		self.STATUS = re.search(
			'%s(.*)%s' % ("Battery "r'\d+'": ", ", "), acpi_report).group(1)

		if self.STATUS == "Unknown":
			AC = self.GetFromShellLong("acpi -a | grep -oP '(?<=: ).*'")
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
			self.TEXT_COLOR = "#FF0000"  # red
		elif int(self.LEVEL) < 20:
			self.TEXT_COLOR = "#FF8000"  # orange, I guess
		else:
			self.TEXT_COLOR = "#FFFFFF"  # white

		if not self.GRAPHICAL:
			self.TEXT = self.LEVEL + "%, " + self.STATUS

	def Dzen(self):
		if self.GRAPHICAL:
			return self.HEADER + self.GetGraphicalBar()
		else:
			self.Format()
			return self.HEADER + "^fg(" + self.TEXT_COLOR + ")" + self.TEXT

	def WidthPxl(self, font):
		if self.GRAPHICAL:
			w = Widget.WidthPxl(self, font) + self.INDICATOR_LENGTH
		else:
			w = Widget.WidthPxl(self, font)
		return w

	def GetGraphicalBar(self):
		drawnbar = int((100 - int(self.LEVEL)) * (self.INDICATOR_LENGTH / 100))
		leftbar = int(int(self.LEVEL) * (self.INDICATOR_LENGTH / 100))

		if int(self.LEVEL) <= 20:
			fgcol = "^fg(" + self.RED + ")"
		else:
			fgcol = "^fg(" + self.GRN + ")"

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
		result = "^fg(white)^p(;4)" + fgcol + "^r(" + str(leftbar) + \
				"x8)^fg(" + self.BAR + ")^r(" + \
				str(drawnbar) + "x8)^p(;-4)"
		return result
