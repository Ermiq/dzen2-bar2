#!/bin/python

import re
from widgets.WidgetBase.WidgetBase import WidgetBase
from config import config

class MemoryWidget(WidgetBase):

	INDICATOR_LENGHT = 50
	SCARCE_THRESHOLD = 95
	USEDBAR = 0
	FREEBAR = 0

	def __init__(self, width, action = ""):
		WidgetBase.__init__(self, width, action)
		self.HEADER = config.RAM_HEADER

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
			self.TEXT_COLOR = config.clrRED
		else:
			self.TEXT_COLOR = config.clrBGR

	def Dzen(self):
		#self.TextFormat()
		self.DZEN2LINE = self.HEADER + \
			"^fg(white)^p(;4)^fg(" + self.TEXT_COLOR + ")^r(" + str(self.USEDBAR) + \
				"x8)^fg(" + config.clrGRN + ")^r(" + str(self.FREEBAR) + "x8)^p(;-4)"
		self.AddAction()
		return self.DZEN2LINE

	def WidthPxl(self, font):
		w = WidgetBase.WidthPxl(self, font) + self.INDICATOR_LENGHT
		return int(w)
