#!/bin/python

import subprocess
from helpers import shellHelper


class WidgetBase:

	TEXT = ""
	HEADER = ""
	ACTION = ""
	DZEN2LINE = ""
	WIDTH = 0
	WIDTH_PXL = 0
	OFFSET = 0
	TEXT_COLOR = ""

	def __init__(self, width, action = ""):
		'''Initialize the object instance.
		And provide the WIDTH value for widget'''
		self.WIDTH = width
		self.ACTION = action

	def TextFormat(self):
		'''Trancate the TEXT if it's too long for the given widget WIDTH
		or (if it's too short) align it at center by addign spaces to left and right'''
		length = len(self.HEADER + self.TEXT)
		maxTextLength = self.WIDTH - len(self.HEADER)
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
		'''Puts a clickable area tag around the widget HEADER+TEXT dzen2 line.
		Use it when the dzen2 line is created for the widget.
		Basically, after the creation of the line in widget's 'Dzen()' function.'''
		self.DZEN2LINE = "^ca(" + self.ACTION + ")" + self.DZEN2LINE + "^ca()"

	def WidthPxl(self, font):
		'''Returns the length (in pixels) of the widget HEADER+TEXT string
		(along with padding spaces), uses 'dzen2-textwidth' tool (usually
		installed with 'dzen2' package).

		Graphical widgets (such as RAM widget) should have empty TEXT, and their
		INDICATOR_WIDTH should be added to the result of this function.

		It doesn't work well with non-monospaced fonts since the width varies with that fonts.

		Also, requires the font to be installed and set properly for X fonts description format system:
		read here: https://github.com/Ermiq/dzen2-bar2/edit/master/README.md

		Also, since 'dzen2-textwidth' doesn't work with cyrillic characters (I believe it won't work with
		any non-latin characters either), we're going to simulate the widget text with a string that consists off
		"x" letters, and has the same amount of characters (i.e. length) as the real widget TEXT string.
		'''
		simulatedText = "x" * len(self.HEADER + self.TEXT)
		self.WIDTH_PXL = int(shellHelper.ExecSplit(
			["dzen2-textwidth", font, simulatedText]))
		return self.WIDTH_PXL
