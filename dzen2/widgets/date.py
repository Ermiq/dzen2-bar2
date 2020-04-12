#!/bin/python

from .widgetBase import Widget

class DateWidget(Widget):

	def __init__(self, width):
		Widget.__init__(self, width)
	
	def Update(self):
		self.TEXT = self.GetFromShellLong("date +'%a, %d %b. %H:%M:%S'")

	def Dzen(self):
		self.Format()
		return self.TEXT

	def WidthPxl(self, font):
		s = "Su, 12 apl. 15:34:25"
		w = self.GetFromShell(["dzen2-textwidth", font, s])
		#w = Widget.WidthPxl(self, font)
		return int(w)
