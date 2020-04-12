#!/bin/python

import subprocess

class Widget:
	TEXT = ""
	HEADER = ""
	WIDTH = 0
	TEXT_COLOR = ""

	def __init__(self, width):
		'''Initialize the object instance.
		And provide the WIDTH value for widget'''
		self.WIDTH = width
	
	def GetFromShell(self, listOfCommands):
		'''Run Linux shell command.
		As an arument it takes a list of strings, e.g., [ "sudo", "apt", "update" ].
		Use it for single commands only. For piped commands use 'GetFromShellLong()' instead.
		Returns the result as string.'''
		out = subprocess.check_output(
			listOfCommands, universal_newlines=True).strip()
		return out
	
	def GetFromShellLong(self, command):
		'''Run Linux shell command.
		This is for complicated combinations of commands, such as "echo "Hello world" | grep Hello".
		Returns the result as string.'''
		out = subprocess.check_output(
			command, shell=True, universal_newlines=True).strip()
		return out

	def Format(self):
		'''Trancate the text if it's too long for the given widget WIDTH
		or (if it's too short) align it at center by addign spaces to left and right'''
		if len(self.TEXT) > self.WIDTH:
			self.TEXT = self.TEXT[0:self.WIDTH]
		else:
			self.TEXT = self.TEXT.center(self.WIDTH, ' ')

	def Update(self):
		pass

	def Dzen(self):
		'''What will be returned to dzen2 line.
		Usually it's just "variableHEADER^fg(#FFFFFF)variableTEXT"
		i.e. print the header text, then set the foreground color to white
		and print the main text of the widget, like date or volume level.'''
		pass
	
	def WidthPxl(self, font):
		'''Returns the length (in pixels) of the overall widget text (with a header and padding spaces).
		Do not use it with graphical widgets such as RAM widget.
		Doesn't work well with non-monospaced fonts since the width varies with that fonts.
		Also, requires the font to be installed and set properly for X fonts description format system:
		read here: https://github.com/Ermiq/dzen2-bar2/edit/master/README.md
		
		Also, since 'dzen2-textwidth' doesn't work with cyrillic characters (I believe it won't work with
		any non-latin characters either), we're going to simulate the widget text with a string that consists off
		"x" characters, and has the same amount of characters (i.e. length) as the widget TEXT.
		'''
		simulatedText = "x" * len(self.HEADER + self.TEXT)
		w = self.GetFromShell(["dzen2-textwidth", font, simulatedText])
		return int(w)