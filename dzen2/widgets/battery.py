#!/bin/python

import re
from .widgetBase import Widget


class BatteryWidget(Widget):

	COLOR = ""
	RETURN_TEXT = True
	LEVEL = 0
	STATUS = ""
	INDICATOR_LENGTH = 50
	GRAPHICAL = True
	SHOW_ARROW = False  # Looks ugly, and block changes the size
	WAS_ARROW = True
	BAR = '#A6F09D'     # green background of bar-graphs
	GRN = '#65A765'     # light green (normal)
	RED = '#FF0000'     # light red/pink (warning)

	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "BAT: "

	def Update(self):
		# 'acpi -b' returns something like: "Battery 0: Charging, 94%".
		BAT_STATUS = self.GetFromShell("acpi -b")
		self.LEVEL = re.findall(r'\d+', BAT_STATUS)[1]
		self.STATUS = re.search(
			'%s(.*)%s' % ("Battery "r'\d+'": ", ", "), BAT_STATUS).group(1)

		if self.STATUS == "Unknown":
			# For Unknown status check AC adapter connectivity state.
			# 'acpi -a' returns "Adapter 0: on-line" or "off-line"
			AC = self.GetFromShell("acpi -a | grep -oP '(?<=: ).*'")
			if AC == "on-line":
				self.STATUS = "Charging"
			elif AC == "off-line":
				self.STATUS = "Discharging"

		'''
		if RETURN_TEXT:
			pass
		else:
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
		global COLOR
		if int(self.LEVEL) < 5:
			COLOR = "#FF0000"  # red
		elif int(self.LEVEL) < 20:
			COLOR = "#FF8000"  # orange, I guess
		else:
			COLOR = "#FFFFFF"  # white

		self.TEXT = self.LEVEL + "%, " + self.STATUS
		self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)

	def Dzen(self):
		if self.GRAPHICAL:
			return self.HEADER + self.GetGraphicalBar()
		else:
			return "^fg(" + COLOR + ")" + self.HEADER + self.TEXT

	def Width(self):
		return self.WIDTH

	def WidthPxl(self, font):
		if self.GRAPHICAL:
			w = self.GetFromShell("dzen2-textwidth " + font + " '" + self.HEADER + "'")
			return int(w) + self.INDICATOR_LENGTH
		else:
			w = self.GetFromShell("dzen2-textwidth " + font +
							  " '" + self.HEADER + self.TEXT + "'")
			return int(w)

	def GetGraphicalBar(self):
		drawnbar = int((100 - int(self.LEVEL)) * (self.INDICATOR_LENGTH / 100))
		leftbar = int(int(self.LEVEL) * (self.INDICATOR_LENGTH / 100))

		if int(self.LEVEL) <= 20:
			fgcol = "^fg(" + self.RED + ")"
		else:
			fgcol = "^fg(" + self.GRN + ")"

		result = "^fg(white)^p(;4)" + fgcol + "^r(" + str(leftbar) + \
				"x8)^fg(" + self.BAR + ")^r(" + \
				str(drawnbar) + "x8)^p(;-4)"
		'''
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
		return result
