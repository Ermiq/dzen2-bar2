#!/bin/python

import subprocess

class Widget:
	"Traratatatatatara"
	TEXT = ""
	HEADER = ""
	WIDTH = 0

	def __init__(self, width):
		self.WIDTH = width

	def GetFromShell(self, processStr):
		out = subprocess.check_output(
			processStr, shell=True, universal_newlines=True).strip()
		return out
	
	def AlignCenter(self, word, desiredLen):
		# >>> width = 20
		# >>> print 'HackerRank'.center(width,'-')
		# -----HackerRank-----
		word = word.center(desiredLen, ' ')
		return word

	def Update(self):
		pass

	def Dzen(self):
		pass

	def Width(self):
		pass

	def WidthPxl(self, font):
		pass