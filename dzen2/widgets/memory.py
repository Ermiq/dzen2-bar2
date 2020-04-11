#!/bin/python

import re
from .widgetBase import Widget

class MemoryWidget(Widget):

	INDICATOR_LENGHT = 50
	SCARCE_THRESHOLD = 95
	BAR = '#A6F09D'     # green background of bar-graphs
	GRN = '#65A765'     # light green (normal)
	RED = '#FF0000'     # light red/pink (warning)

	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "RAM: "

	def Update(self):
		totalRAM = 0
		freeRAM = 0
		with open("/proc/meminfo") as origin_file:
			for line in origin_file:
				if re.search(r'MemTotal:', line):
					line = re.findall(r'\d+', line)
					if line:
						totalRAM = int(line[0])
				else:
					if re.search(r'MemFree:', line):
						line = re.findall(r'\d+', line)
						if line:
							freeRAM = int(line[0])

		usedRAM = totalRAM - freeRAM
		usedbar = int(usedRAM * self.INDICATOR_LENGHT / totalRAM)
		freebar = int(freeRAM * self.INDICATOR_LENGHT / totalRAM)

		if usedbar >= (self.INDICATOR_LENGHT / 100 * self.SCARCE_THRESHOLD):
			fgcol = "^fg(" + self.RED + ")"
		else:
			fgcol = "^fg(" + self.GRN + ")"
		self.TEXT = "^fg(white)^p(;4)" + fgcol + "^r(" + str(usedbar) + \
			"x8)^fg(" + self.BAR + ")^r(" + str(freebar) + "x8)^p(;-4)"
		self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)

	def Dzen(self):
		return self.HEADER + self.TEXT

	def Width(self):
		return self.WIDTH

	def WidthPxl(self, font):
	    w = self.GetFromShell("dzen2-textwidth " + font + " '" + self.HEADER + "'")
	    return int(w) + self.INDICATOR_LENGHT
