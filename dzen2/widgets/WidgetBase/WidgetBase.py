#!/bin/python

import subprocess
from helpers import shellHelper

class WidgetBase:

	TEXT = ""
	HEADER = ""
	TAIL = ""

	ACTION = ""
	DZEN2LINE = ""
	
	WIDTH = 0
	WIDTH_PXL = 0
	OFFSET = 0
	
	TEXT_COLOR = ""

	def __init__(self, width, action = ""):
		'''Widget instance initialization.
		Provide the WIDTH value for widget (in chars not pixels)
		and action to perform (e.g., "1, firefox").
		'''
		self.WIDTH = width
		self.ACTION = action

	def TextFormat(self):
		'''Trancate the TEXT if it's too long to fit the widget WIDTH
		or (if it's too short) align it at center by addign spaces to left and right.\n
		Widget's HEADER and TAIL do affect the resulting text length, but
		they are not trancated. If WIDTH is set to 0, then TEXT will be erased
		but HEADER and TAIL will remain.'''
		length = len(self.HEADER + self.TEXT + self.TAIL)
		maxTextLength = self.WIDTH - len(self.HEADER + self.TAIL)
		if length > self.WIDTH:
			self.TEXT = self.TEXT[0:maxTextLength]
		else:
			self.TEXT = self.TEXT.center(maxTextLength, ' ')

	def Update(self):
		pass

	def Dzen(self):
		'''What will be returned to dzen2 line.
		Usually it's just "variableHEADER^fg(#FFFFFF)variableTEXT"
		i.e. print the header text, then set the foreground color to white
		and print the main text of the widget such as date or volume level.'''
		pass

	def AddAction(self):
		'''Puts a clickable area tag around the widget TEXT dzen2 line.\n
		Use it when the dzen2 line text is ready for the widget.'''
		self.DZEN2LINE = "^ca(" + self.ACTION + ")" + self.DZEN2LINE + "^ca()"
	
	def ActionCustomZone(self, string = "", action = ""):
		'''Puts a clickable area tag around the given text.\n
		Use it to add actions to HEADER and TAIL. The TEXT area is managed by 'AddAction(self)'.'''
		string = "^ca(" + action + ")" + string + "^ca()"
		return string

	def WidthPxl(self, font):
		'''Returns the length (in pixels) of the widget HEADER+TEXT string
		(along with padding spaces), uses 'dzen2-textwidth' tool (usually
		installed with 'dzen2' package).\n
		Graphical widgets (such as RAM widget) should have empty TEXT, and their
		INDICATOR_WIDTH should be added to the result of this function.\n
		It doesn't work well with non-monospaced fonts since the width varies with that fonts.\n
		Also, requires the font to be installed and set properly for X fonts description format system:
		read here: https://github.com/Ermiq/dzen2-bar2/edit/master/README.md\n
		Also, since 'dzen2-textwidth' doesn't work with cyrillic characters (I believe it won't work with
		any non-latin characters either), we're going to simulate the widget text with a string that consists off
		"x" letters, and has the same amount of characters (i.e. length) as the real widget TEXT string.
		'''
		simulatedText = "x" * len(self.HEADER + self.TEXT + self.TAIL)
		self.WIDTH_PXL = int(shellHelper.ExecSplit(
			["dzen2-textwidth", font, simulatedText]))
		return self.WIDTH_PXL
