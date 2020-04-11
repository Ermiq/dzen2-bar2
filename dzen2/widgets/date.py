#!/bin/python

from .widgetBase import Widget

class DateWidget(Widget):

	def __init__(self, width):
		Widget.__init__(self, width)
	
	def Update(self):
		self.TEXT = self.GetFromShell("date +'%a, %d %b. %H:%M:%S'")
		self.TEXT = self.AlignCenter(self.TEXT, self.WIDTH)

	def Dzen(self):
		return self.TEXT

	def Width(self):
		return self.WIDTH

	def WidthPxl(self, font):
		# dzen2-textwidth seems to don't know about non-latin languages, therefore returns
		# lenght of 0(zero) if the string consists off cyrillic symbols for example.
		# So, gotta emulate the string manually then:
		date = self.AlignCenter("Tu, 12 apl, 23:45:19", self.WIDTH)
		w = self.GetFromShell("dzen2-textwidth " + font + " '" + date + "'")
		#w = self.GetFromShell("dzen2-textwidth " + font + ' "' + self.TEXT + '"')
		return int(w)
