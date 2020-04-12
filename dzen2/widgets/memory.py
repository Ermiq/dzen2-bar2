#!/bin/python

import re
from .widgetBase import Widget

class MemoryWidget(Widget):

	INDICATOR_LENGHT = 50
	SCARCE_THRESHOLD = 95
	BAR = '#A6F09D'     # green background of bar-graphs
	GRN = '#65A765'     # light green (normal)
	RED = '#FF0000'     # light red/pink (warning)
	USEDBAR = 0
	FREEBAR = 0

	def __init__(self, width):
		Widget.__init__(self, width)
		self.HEADER = "RAM: "

	def Update(self):
		self.TEXT = ""
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
		self.USEDBAR = int(usedRAM * self.INDICATOR_LENGHT / totalRAM)
		self.FREEBAR = int(freeRAM * self.INDICATOR_LENGHT / totalRAM)

		if self.USEDBAR >= (self.INDICATOR_LENGHT / 100 * self.SCARCE_THRESHOLD):
			self.TEXT_COLOR = "^fg(" + self.RED + ")"
		else:
			self.TEXT_COLOR = "^fg(" + self.GRN + ")"

	def Dzen(self):
		#self.Format()
		return self.HEADER + \
			"^fg(white)^p(;4)" + self.TEXT_COLOR + "^r(" + str(self.USEDBAR) + \
				"x8)^fg(" + self.BAR + ")^r(" + str(self.FREEBAR) + "x8)^p(;-4)"

	def WidthPxl(self, font):
		w = Widget.WidthPxl(self, font) + self.INDICATOR_LENGHT
		return int(w)
